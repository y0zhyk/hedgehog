$(document).ready ->
  showErrorMessage()

showErrorMessage = () ->
  $("div.error").fadeIn().delay(5000).fadeOut()