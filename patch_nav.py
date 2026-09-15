# -*- coding: utf-8 -*-
with open('src/components/layout/navbar.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

import re
old_links = '''  const links = [
    { href: "/", label: "Home" },
    { href: "/papers", label: "Papers" },
    { href: "/calculator", label: "Calculator" },
    { href: "/developers", label: "Developers" },
    { href: "/contributors", label: "Contributors" },
    { href: "/about", label: "About" },
  ];'''

new_links = '''  const links = [
    { href: "/", label: "Home" },
    { href: "/markai", label: "MarkAi" },
    { href: "/calculator", label: "Calculator" },
    { href: "/developers", label: "Developers" },
  ];'''

code = code.replace(old_links, new_links)

with open('src/components/layout/navbar.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
