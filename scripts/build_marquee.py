"""Builds assets/tech-marquee.svg: a seamless horizontal carousel moving left to right.
Needs: npm i devicon@2.16.0   usage: python3 scripts/build_marquee.py <.../node_modules/devicon/icons>"""
import re, sys, pathlib
ICONS = pathlib.Path(sys.argv[1])
NAMES = ["csharp","typescript","python","cplusplus","c","java","javascript","r",
         "nextjs","react","tailwindcss","html5","css3","dotnetcore","postgresql","redis","mysql",
         "docker","nginx","cloudflare","amazonwebservices","redhat","ubuntu","githubactions","git","figma"]
T, GAP, W, H = 64, 18, 960, 100
STEP = T + GAP; LOOP = STEP * len(NAMES)
def load(name, uid):
    f = ICONS/name/f"{name}-original.svg"
    if not f.exists(): f = ICONS/name/f"{name}-original-wordmark.svg"
    s = f.read_text(); vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    body = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    body = re.sub(r'<\?xml.*?\?>|<!--.*?-->', '', body, flags=re.S)
    for i in set(re.findall(r'id="([^"]+)"', body)):
        body = body.replace(f'id="{i}"', f'id="{uid}{i}"').replace(f'url(#{i})', f'url(#{uid}{i})').replace(f'href="#{i}"', f'href="#{uid}{i}"')
    return vb, body
def strip(copy):
    o = []
    for k, n in enumerate(NAMES):
        vb, body = load(n, f"c{copy}i{k}_")
        x = k*STEP
        o.append(f'<g transform="translate({x},{(H-T)/2})"><rect width="{T}" height="{T}" rx="15" fill="#f4f2ee" stroke="#e1ded8"/>'
                 f'<svg x="12" y="12" width="{T-24}" height="{T-24}" viewBox="{vb}">{body}</svg></g>')
    return "".join(o)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Technologies I use, scrolling">'
 f'<style>.t{{animation:slide 55s linear infinite}}@keyframes slide{{from{{transform:translateX(-{LOOP}px)}}to{{transform:translateX(0)}}}}'
 '@media (prefers-reduced-motion:reduce){.t{animation:none}}</style>'
 f'<defs><linearGradient id="f"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".08" stop-color="#fff"/><stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
 f'<mask id="m"><rect width="{W}" height="{H}" fill="url(#f)"/></mask></defs>'
 f'<g mask="url(#m)"><g class="t">{strip(0)}<g transform="translate({LOOP},0)">{strip(1)}</g></g></g></svg>')
pathlib.Path("assets/tech-marquee.svg").write_text(svg); print(len(svg)//1024, "KB")
