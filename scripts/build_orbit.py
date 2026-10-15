"""Builds assets/tech-orbit.svg (animated, self-contained). Needs: npm i devicon@2.16.0"""
import math, re, sys, pathlib
ICONS = pathlib.Path(sys.argv[1])  # .../node_modules/devicon/icons
RINGS = [  # (radius, seconds, direction, icons)
  (118, 48,  1, ["nextjs","react","tailwindcss","html5","css3","dotnetcore"]),
  (212, 72, -1, ["csharp","typescript","python","cplusplus","c","java","javascript","r","postgresql","redis"]),
  (306, 100, 1, ["mysql","docker","nginx","cloudflare","amazonwebservices","redhat","ubuntu","githubactions","git","figma"]),
]
W, H, CX, CY, T = 760, 760, 380, 380, 58
def load(name, uid):
    f = ICONS/name/f"{name}-original.svg"
    if not f.exists(): f = ICONS/name/f"{name}-original-wordmark.svg"
    s = f.read_text()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    body = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    body = re.sub(r'<\?xml.*?\?>|<!--.*?-->', '', body, flags=re.S)
    for i in set(re.findall(r'id="([^"]+)"', body)):
        body = body.replace(f'id="{i}"', f'id="{uid}{i}"').replace(f'url(#{i})', f'url(#{uid}{i})').replace(f'href="#{i}"', f'href="#{uid}{i}"')
    return vb, body
out = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack orbit">',
'<style>.o{transform-origin:0 0;animation:spin var(--d) linear infinite}.c{transform-origin:0 0;animation:spin var(--d) linear infinite}',
'.cw{animation-direction:normal}.ccw{animation-direction:reverse}',
'@keyframes spin{to{transform:rotate(360deg)}}@keyframes pulse{50%{opacity:.35;transform:scale(1.25)}}',
'.p{transform-origin:0 0;animation:pulse 3s ease-in-out infinite}',
'@media (prefers-reduced-motion:reduce){.o,.c,.p{animation:none}}</style>',
f'<g transform="translate({CX},{CY})">']
for r,_,_,_ in RINGS: out.append(f'<circle r="{r}" fill="none" stroke="#a9a6a0" stroke-opacity=".45" stroke-dasharray="3 7"/>')
out.append('<circle class="p" r="46" fill="#FF7A59" fill-opacity=".18"/><circle r="30" fill="#FF7A59"/>')
out.append('<text y="5" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="13" font-weight="700" letter-spacing="2" fill="#3A1206">STACK</text>')
n = 0
for ri,(r,sec,d,names) in enumerate(RINGS):
    cls = "o" + (" ccw" if d<0 else "")
    out.append(f'<g class="{cls}" style="--d:{sec}s">')
    for k,name in enumerate(names):
        a = 2*math.pi*k/len(names) - math.pi/2 + ri*0.4
        x, y = r*math.cos(a), r*math.sin(a)
        vb, body = load(name, f"i{n}_"); n += 1
        out.append(f'<g transform="translate({x:.1f},{y:.1f})"><g class="c{" ccw" if d>0 else ""}" style="--d:{sec}s">'
                   f'<rect x="{-T/2}" y="{-T/2}" width="{T}" height="{T}" rx="14" fill="#f4f2ee" stroke="#e1ded8"/>'
                   f'<svg x="{-T/2+11}" y="{-T/2+11}" width="{T-22}" height="{T-22}" viewBox="{vb}">{body}</svg></g></g>')
    out.append('</g>')
out.append('</g></svg>')
pathlib.Path("assets/tech-orbit.svg").write_text("".join(out))
print(len("".join(out))//1024, "KB")
