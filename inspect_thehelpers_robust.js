const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const results = {
    total_semesters: 0,
    semester_urls: [],
    sample_subjects: [],
    requires_browser_automation: true,
    resource_types_found: [],
    hosting_services: []
  };

  try {
    console.log('=== HOMEPAGE ===');
    await page.goto('https://thehelpers.tech/', { waitUntil: 'networkidle', timeout: 45000 });
    await page.waitForTimeout(3000);

    // Save HTML for debugging
    const homeHtml = await page.content();
    fs.writeFileSync('C:\\Users\\ASUS\\Desktop\\system\\thehelpers_home.html', homeHtml);
    console.log('Saved homepage HTML');

    // Try multiple strategies to find semester links
    console.log('\nSearching for semester links...');

    // Strategy 1: Look for any links with "semester" text
    const textLinks = await page.$$eval('a', els =>
      els.map(a => ({ text: a.textContent.trim(), href: a.href }))
         .filter(l => l.text.toLowerCase().includes('semester') || /semester.*\d/.test(l.text.toLowerCase()))
    );
    console.log('Links with "semester" text:', textLinks.length);

    // Strategy 2: Look for links matching /semesters/N pattern
    const patternLinks = await page.$$eval('a', els =>
      els.map(a => a.href)
         .filter(href => /\/semesters\/\d+/.test(href))
    );
    console.log('Links matching /semesters/\\d+ pattern:', patternLinks.length);

    // Strategy 3: Check if page uses divs or buttons instead of links
    const allText = await page.evaluate(() => document.body.innerText);
    const semesterMentions = (allText.match(/semester\s*\d+/gi) || []);
    console.log('Text mentions of semesters:', semesterMentions.slice(0, 10));

    // Extract unique semester URLs
    const semesterSet = new Set();
    patternLinks.forEach(href => {
      const match = href.match(/(https?:\/\/[^/]+\/semesters\/\d+)/);
      if (match) semesterSet.add(match[1]);
    });

    // If no links found, try to construct URLs from numbers 1-8
    if (semesterSet.size === 0) {
      console.log('\nNo semester links found, trying direct navigation...');
      for (let i = 1; i <= 8; i++) {
        const testUrl = `https://thehelpers.tech/semesters/${i}`;
        try {
          const response = await page.goto(testUrl, { waitUntil: 'networkidle', timeout: 30000 });
          if (response.status() !== 404) {
            semesterSet.add(testUrl);
            console.log(`✓ Semester ${i} exists`);
          }
        } catch (e) {
          console.log(`✗ Semester ${i} failed: ${e.message}`);
        }
      }
    }

    results.semester_urls = Array.from(semesterSet).sort();
    results.total_semesters = results.semester_urls.length;

    console.log(`\nFound ${results.total_semesters} semesters`);
    results.semester_urls.forEach(url => console.log(`  - ${url}`));

    // Sample semesters 3, 5, 7
    const sampleSemNums = [3, 5, 7];

    for (const semNum of sampleSemNums) {
      console.log(`\n=== SEMESTER ${semNum} ===`);
      const semUrl = `https://thehelpers.tech/semesters/${semNum}`;

      await page.goto(semUrl, { waitUntil: 'networkidle', timeout: 45000 });
      await page.waitForTimeout(3000);

      // Save HTML for debugging
      fs.writeFileSync(`C:\\Users\\ASUS\\Desktop\\system\\semester_${semNum}.html`, await page.content());

      // Find subject links
      const allLinks = await page.$$eval('a', els =>
        els.map(a => ({ text: a.textContent.trim(), href: a.href }))
      );

      const subjects = allLinks.filter(l => {
        const match = l.href.match(/\/semesters\/(\d+)\/([^/?#]+)/);
        return match && parseInt(match[1]) === semNum && match[2] && match[2] !== String(semNum);
      });

      // Deduplicate by href
      const uniqueSubjects = Array.from(
        new Map(subjects.map(s => [s.href, s])).values()
      );

      console.log(`Found ${uniqueSubjects.length} subjects`);
      uniqueSubjects.slice(0, 10).forEach(s => console.log(`  - ${s.text} | ${s.href}`));

      const semesterData = {
        semester: semNum,
        subject_count: uniqueSubjects.length,
        subjects: []
      };

      // Sample first 2-3 subjects
      const samplesToTake = Math.min(3, uniqueSubjects.length);

      for (let i = 0; i < samplesToTake; i++) {
        const subject = uniqueSubjects[i];
        console.log(`\n  Subject ${i + 1}: ${subject.text}`);
        console.log(`  URL: ${subject.href}`);

        await page.goto(subject.href, { waitUntil: 'networkidle', timeout: 45000 });
        await page.waitForTimeout(3000);

        // Find resource links
        const resLinks = await page.$$eval('a', els =>
          els.map(a => ({
            text: a.textContent.trim(),
            href: a.href,
            title: a.getAttribute('title') || '',
            ariaLabel: a.getAttribute('aria-label') || ''
          }))
        );

        const resources = resLinks.filter(l => {
          const text = (l.text || '').toLowerCase();
          const href = (l.href || '').toLowerCase();
          return (
            href.includes('drive.google') ||
            href.includes('pyq') ||
            href.includes('ct-') ||
            href.includes('/notes') ||
            text.includes('pyq') ||
            text.includes('ct ') ||
            text.includes('notes') ||
            text.includes('paper') ||
            text.includes('previous year')
          );
        });

        const uniqueRes = Array.from(
          new Map(resources.map(r => [r.href, r])).values()
        );

        console.log(`  Found ${uniqueRes.length} resources`);

        const resourceList = uniqueRes.slice(0, 5).map(r => {
          const text = (r.text || '').toLowerCase();
          const href = (r.href || '').toLowerCase();

          let type = 'Resource';
          if (href.includes('pyq') || text.includes('pyq') || text.includes('previous year')) {
            type = 'PYQ';
            if (!results.resource_types_found.includes('PYQ (Previous Year Questions)')) {
              results.resource_types_found.push('PYQ (Previous Year Questions)');
            }
          } else if (href.includes('ct') || text.includes('ct ') || text.includes('class test')) {
            type = 'CT';
            if (!results.resource_types_found.includes('CT (Class Test)')) {
              results.resource_types_found.push('CT (Class Test)');
            }
          } else if (href.includes('notes') || text.includes('notes')) {
            type = 'Notes';
            if (!results.resource_types_found.includes('Notes')) {
              results.resource_types_found.push('Notes');
            }
          }

          if (r.href.includes('drive.google') && !results.hosting_services.includes('Google Drive')) {
            results.hosting_services.push('Google Drive');
          }

          console.log(`    - [${type}] ${r.text}`);
          console.log(`      ${r.href.substring(0, 80)}`);

          return {
            title: r.text,
            type: type,
            url_pattern: r.href
          };
        });

        semesterData.subjects.push({
          name: subject.text,
          url: subject.href,
          resources: resourceList
        });
      }

      results.sample_subjects.push(semesterData);
    }

    // Calculate estimates
    const totalSubjectCount = results.sample_subjects.reduce((sum, s) => sum + s.subject_count, 0);
    results.estimated_subjects_per_semester = totalSubjectCount > 0
      ? Math.round(totalSubjectCount / results.sample_subjects.length)
      : 0;

    // Estimate total resources (assuming ~3-5 resources per subject)
    const avgResourcesPerSubject = 4;
    results.estimated_total_resources = results.estimated_subjects_per_semester *
                                       results.total_semesters *
                                       avgResourcesPerSubject;

    console.log('\n=== FINAL RESULTS ===');
    console.log(JSON.stringify(results, null, 2));

    // Write detailed results
    fs.writeFileSync(
      'C:\\Users\\ASUS\\Desktop\\system\\inspection_results.json',
      JSON.stringify(results, null, 2)
    );
    console.log('\nResults saved to inspection_results.json');

  } catch (error) {
    console.error('Error:', error.message);
    console.error(error.stack);
  } finally {
    await browser.close();
  }
})();
