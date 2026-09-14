# -*- coding: utf-8 -*-
with open('src/app/developers/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# We need to replace the DeveloperCard component
new_card = '''
function DeveloperCard({ dev }: { dev: any }) {
  const [isAngry, setIsAngry] = useState(false);

  const handleTrigger = () => {
    if (isAngry) return;
    setIsAngry(true);
    
    const msg = dev.name.includes("Aditya") ? "Listening to music 🎧" : "Larping 🧙‍♂️";
    toast(msg, { 
      duration: 1200, 
      style: { fontSize: "13px", padding: "8px 14px", minHeight: "36px", width: "fit-content", margin: "0 auto" }
    });
    
    setTimeout(() => {
      setIsAngry(false);
    }, 1200);
  };

  return (
    <div className="bg-card border border-border rounded-2xl p-8 flex flex-col items-center text-center gap-5 hover:border-accent/30 transition-colors">
      <img 
        src={dev.avatar} 
        alt={dev.name} 
        onClick={handleTrigger}
        onMouseEnter={handleTrigger}
        className={w-20 h-20 rounded-full border-2 border-accent/20 object-cover cursor-pointer transition-all duration-[1200ms] ease-out } 
      />

      <div>
        <h3 className="text-xl font-semibold text-accent">{dev.name}</h3>
      </div>

      <p className="text-sm text-muted-foreground leading-relaxed">{dev.contribution}</p>

      <div className="flex items-center gap-5 pt-4 mt-auto border-t border-border w-full justify-center">
        {dev.github && (
          <Link href={https://github.com/} target="_blank" className="text-muted-foreground hover:text-accent transition-colors">
            <GithubIcon />
          </Link>
        )}
        {dev.linkedin && (
          <Link href={https://linkedin.com/in/} target="_blank" className="text-muted-foreground hover:text-accent transition-colors">
            <LinkedinIcon />
          </Link>
        )}
        {dev.instagram && (
          <Link href={https://instagram.com/} target="_blank" className="text-muted-foreground hover:text-accent transition-colors">
            <InstagramIcon />
          </Link>
        )}
      </div>
    </div>
  );
}
'''

# Find the old DeveloperCard function and replace it
card_pattern = r'function DeveloperCard\(\{ dev \}: \{ dev: any \}\) \{.*?(?=\nexport default function DevelopersPage)'
code = re.sub(card_pattern, new_card.strip() + '\n\n', code, flags=re.DOTALL)

with open('src/app/developers/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
