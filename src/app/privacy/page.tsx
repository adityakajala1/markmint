"use client";

import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";

export default function PrivacyPage() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <Navbar />
      <main className="flex-1 w-full px-6 md:px-10 pt-8 pb-32">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-8">Privacy Policy</h1>
        
        <div className="prose prose-invert max-w-none text-muted-foreground space-y-6 text-sm leading-relaxed text-justify">
          <p><strong>Effective Date: September 15, 2026</strong></p>
          
          <p>
            MarkMint ("we", "our", or "us") is deeply committed to protecting your privacy and ensuring the cryptographic security of your personal and academic data. This exhaustive Privacy Policy outlines our uncompromising practices regarding the collection, use, processing, retention, and disclosure of your information when you utilize our digital web properties, the Mint+ Calculator, and the MintAi conversational service. By choosing to use the Service, you signify your explicit consent to the data practices described in this document.
          </p>

          <h2 className="text-xl font-bold text-foreground mt-8 mb-4">1. Expansive Information Collection and Algorithmic Processing</h2>
          <p>
            We collect several distinct categories of information for varied operational and developmental purposes to provide, refine, and secure our Service. This includes, but is not limited to, academic parameters such as your selected engineering branch, semester progression data, target GPA metrics, course selections, and the nuanced linguistic queries submitted directly to the MintAi models. By engaging with our generative AI interfaces, you grant us explicit, revocable consent to ingest and process the inputted text strings. This data is utilized strictly for the purpose of generating academic responses, fine-tuning our predictive heuristics, and improving the contextual accuracy of future CT and FT paper predictions.
          </p>

          <h2 className="text-xl font-bold text-foreground mt-8 mb-4">2. Usage Data, Telemetry, and Session Diagnostics</h2>
          <p>
            In addition to explicitly provided academic data, our infrastructure automatically harvests information regarding how the Service is accessed, navigated, and utilized ("Usage Data"). This automated telemetry may encompass granular data points such as your device's Internet Protocol (IP) address, browser user-agent string, exact timestamps of page requests, the sequential flow of your navigation through our routing architecture, time spent dwelling on specific calculator outputs, unique device identifiers, hardware footprinting, and other related diagnostic metrics necessary to ensure server stability and mitigate distributed denial-of-service (DDoS) vectors.
          </p>

          <h2 className="text-xl font-bold text-foreground mt-8 mb-4">3. Tracking Technologies, Stateful Cookies, and Local Storage</h2>
          <p>
            We deploy a combination of first-party cookies, session storage, local storage, and similar cryptographic tracking technologies to maintain session continuity, track analytical activity on our Service, and persist specific user preferences. Cookies are localized files containing microscopic amounts of data which may include an anonymized unique identifier. You maintain absolute sovereignty over your browser settings and may instruct your client to refuse all cookies or to alert you when a cookie is being transmitted. However, you acknowledge that refusing these operational cookies may catastrophically degrade your user experience and render the Mint+ Calculator completely inoperable.
          </p>

          <h2 className="text-xl font-bold text-foreground mt-8 mb-4">4. Rigorous Data Retention and Cryptographic Security</h2>
          <p>
            MarkMint will retain your Personal and Academic Data only for the exact temporal duration necessary to fulfill the purposes delineated in this Privacy Policy. We will retain and utilize your Usage Data to the extent mandated by compliance with our legal obligations, dispute resolution proceedings, and the enforcement of our Terms and Conditions. The cryptographic security of your data in transit and at rest is of paramount importance to our engineering philosophy. However, you must acknowledge that no methodology of transmission over the public Internet, nor any form of electronic cloud storage, is mathematically guaranteed to be 100% impenetrable. While we deploy commercially superior defensive perimeters, we cannot insure its absolute, uncompromisable security.
          </p>

          <h2 className="text-xl font-bold text-foreground mt-8 mb-4">5. Third-Party Infrastructure and Service Providers</h2>
          <p>
            We may legally retain and employ third-party corporate entities and independent contractors to facilitate our technological architecture ("Service Providers"), to provision the Service on our behalf, to perform infrastructure-related maintenance, or to assist us in analyzing the macro-trends of how our Service is utilized. These third-party entities are granted restricted, heavily monitored access to your Personal Data strictly to execute these specific tasks on our behalf and are bound by stringent non-disclosure agreements not to disseminate, exploit, or process your data for any ulterior motive. We unequivocally, resolutely do not sell your personal data to third-party advertising brokers, data aggregators, or external marketing conglomerates.
          </p>

          <h2 className="text-xl font-bold text-foreground mt-8 mb-4">6. Policy Iteration and Notification Protocols</h2>
          <p>
            The digital landscape is volatile, and as such, we reserve the inalienable right to iteratively update our Privacy Policy at any chronological juncture. We will notify you of any material changes by publishing the revised Privacy Policy on this exact unified resource identifier (URI). You are strongly advised and legally encouraged to review this Privacy Policy periodically for any structural or linguistic changes. Modifications to this Privacy Policy are considered immediately legally effective the millisecond they are committed and deployed to this web asset.
          </p>
        </div>
      </main>
      <Footer />
    </div>
  );
}
