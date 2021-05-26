import os

# Some functions to insert in to the docs via Jinja2. For example:
# {{fioctl_version() }} will place the fioctl_version number into the markdown
# file in which it is called.

def define_env(env):
  "Functions for MkDocs Jinja2"

  @env.macro
  def fioctl_version():
      import urllib.request, json, os

      ver = os.environ.get("FIOCTL_VERSION")
      if ver:
          return ver

      url = "https://api.github.com/repos/foundriesio/fioctl/releases/latest"
      response = urllib.request.urlopen(url)
      data = json.loads(response.read())

      return data['tag_name']

  @env.macro
  def dummy_function():
      return str(os.getenv("example_variable"))
