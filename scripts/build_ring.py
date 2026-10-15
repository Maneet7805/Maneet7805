"""Builds assets/tech-ring.svg: an inward-curving 3D ring carousel (you look at the inside of the far wall).
The near half of the ring is hidden and everything moves left to right.
Needs: npm i devicon@2.16.0   usage: python3 scripts/build_ring.py <.../node_modules/devicon/icons>"""
import math, re, sys, pathlib
ICONS = pathlib.Path(sys.argv[1])
NAMES = ["csharp","typescript","python","cplusplus","c","java","javascript","r",
         "nextjs","react","tailwindcss","html5","css3","dotnetcore","postgresql","redis","mysql",
         "docker","nginx","cloudflare","amazonwebservices","redhat","ubuntu","githubactions","git","figma"]
W, H, CX, CY = 940, 118, 470, 74
R, RISE, T = 430, 26, 72        # ring radius, how much the middle rises, tile size
DUR, N = 80, 120                # seconds per revolution, keyframes per revolution
def load(name, uid):
    f = ICONS/name/f"{name}-original.svg"
    if not f.exists(): f = ICONS/name/f"{name}-original-wordmark.svg"
    s = f.read_text(); vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    body = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    body = re.sub(r'<\?xml.*?\?>|<!--.*?-->', '', body, flags=re.S)
    for i in set(re.findall(r'id="([^"]+)"', body)):
        body = body.replace(f'id="{i}"', f'id="{uid}{i}"').replace(f'url(#{i})', f'url(#{uid}{i})').replace(f'href="#{i}"', f'href="#{uid}{i}"')
    return vb, body
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Technologies I use, rotating inside a ring">']
for k, n in enumerate(NAMES):
    vb, body = load(n, f"i{k}_")
    pos, scl, opa = [], [], []
    for j in range(N+1):
        th = 2*math.pi*k/len(NAMES) + 2*math.pi*j/N
        d = math.cos(th)                       # 1 = far wall centre, 0 = edge-on, <0 = near wall (hidden)
        e = 1 - d*d if d > 0 else 1            # 0 in the middle, 1 at the sides
        x, y = CX + R*math.sin(th), CY - RISE*max(d, 0)
        sx = max(d, 0.02) * (1 + 0.25*e)       # panels angle toward the viewer at the sides
        sy = 0.88 + 0.28*e                     # and look a little closer/taller there
        pos.append(f"{x:.1f} {y:.1f}"); scl.append(f"{sx:.3f} {sy:.3f}")
        opa.append(f"{min(max((d-0.12)/0.28, 0), 1):.2f}")
    t = f'dur="{DUR}s" repeatCount="indefinite"'
    out.append(f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(pos)}" {t}/>'
               f'<animate attributeName="opacity" values="{";".join(opa)}" {t}/>'
               f'<g><animateTransform attributeName="transform" type="scale" values="{";".join(scl)}" {t}/>'
               f'<rect x="{-T/2}" y="{-T/2}" width="{T}" height="{T}" rx="15" fill="#f4f2ee" stroke="#e1ded8"/>'
               f'<svg x="{-T/2+12}" y="{-T/2+12}" width="{T-24}" height="{T-24}" viewBox="{vb}">{body}</svg></g></g>')
out.append('</svg>')
svg = "".join(out); pathlib.Path("assets/tech-ring.svg").write_text(svg); print(len(svg)//1024, "KB")
