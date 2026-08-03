# Brújula Vocacional Colombia — GitHub Pages

Sitio estático preparado como fuente pública de conocimiento para Microsoft 365 Copilot Agent Builder.

## Repositorio recomendado

- Propietario: `DanteBurbano27`
- Nombre: `brujula-vocacional-knowledge`
- Visibilidad: **Public**
- URL esperada: `https://danteburbano27.github.io/brujula-vocacional-knowledge/`

## Publicación desde el navegador

1. Crea un repositorio público llamado `brujula-vocacional-knowledge`.
2. Extrae el ZIP entregado.
3. En el repositorio, selecciona **Add file > Upload files**.
4. Arrastra **el contenido interno de esta carpeta**, no la carpeta contenedora ni el ZIP.
5. Confirma que `index.html` quede en la raíz del repositorio.
6. Escribe un mensaje de commit y selecciona **Commit changes**.
7. Entra en **Settings > Pages**.
8. En **Build and deployment**, selecciona:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/ (root)`
9. Guarda y espera a que GitHub muestre el enlace **Visit site**.

Todos los archivos incluidos quedan por debajo de 25 MiB. El segundo PDF fue optimizado para web, pero conserva sus 172 páginas y texto extraíble.

## Configuración en Agent Builder

Agrega como sitio específico:

`https://danteburbano27.github.io/brujula-vocacional-knowledge/`

Configura:

- `Search all websites`: OFF
- `Only use specified sources`: ON

La recuperación pública depende de la indexación de Bing. El sitio contiene HTML semántico, `robots.txt` y `sitemap.xml` para facilitar la indexación, pero esta puede no ser inmediata.

## Estructura

- `index.html`: portada y mapa del conocimiento.
- `exploracion-intereses-ria-sec.html`: versión HTML de la capa editorial del Compendio 1.
- `acompanamiento-contexto-colombia.html`: versión HTML de la capa editorial del Compendio 2.
- `fuentes-licencias.html`: atribuciones, licencias y limitaciones.
- `documents/`: compendios PDF completos.
- `robots.txt` y `sitemap.xml`: soporte de indexación.
- `.nojekyll`: evita procesamiento innecesario mediante Jekyll.

## Uso y licencias

El sitio es un prototipo educativo no comercial. Consulta `fuentes-licencias.html` antes de reutilizar o adaptar los materiales.
