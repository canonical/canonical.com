# Templatefinder

The templatefinder can be used to automatically map `.html` and `.md` files to url on a website.
When included the finder will search for files at the given url in a specified template directory.

E.g. `localhost/pages/test` will look for the following files, in order:
- `$TEMPLATE_FOLDER/pages/test.html`
- `$TEMPLATE_FOLDER/pages/test/index.html`
- `$TEMPLATE_FOLDER/pages/test.md`
- `$TEMPLATE_FOLDER/pages/test/index.md`

## Markdown
In case you would like to use markdown for a page, the frontmatter of the Markdown file will need to specify an **HTML** wrapper file, where its contents will be included.
Specify it like so:
```
---
wrapper_template: 'partial/markdown_wrapper.html'
---
```

To output the content inside the wrapper use `{{content | safe}}`.

## Usage

To register the template finder in your Flask app you need to register the template folder in the application config, and specify which routes should be handled by it.
The following example will handle everything via the templatefinder:
```
TEMPLATE_FOLDER = path.join(getcwd(), "templates")

app = Flask(
    template_folder=TEMPLATE_FOLDER,
    static_folder="./static",
)
app.config["TEMPLATE_FOLDER"] = TEMPLATE_FOLDER

template_finder_view = TemplateFinder.as_view("template_finder")
app.add_url_rule("/", view_func=template_finder_view)
app.add_url_rule("/<path:subpath>", view_func=template_finder_view)
```

## Tests
Tests can be run with pytest. This module is using [poetry](https://poetry.eustace.io/), so you can use `poetry run pytest` to execute them easily.
