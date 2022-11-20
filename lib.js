SERVER = "http://127.0.0.1:5000"

function get(url, func) {
  return $.get(SERVER + "/" + url, func)
}
