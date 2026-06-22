package main

import (
	"html/template"
	"net/http"
)

type PageData struct {
	Result string
}

func homePage(w http.ResponseWriter, r *http.Request) {
	tmpl := template.Must(template.ParseFiles("templates/index.html"))
	tmpl.Execute(w, nil)
}
func generate(w http.ResponseWriter, r *http.Request) {
	text := r.FormValue("text")
	banner := r.FormValue("banner")

	fontMap, err := LoadBanner("banner/" + banner + ".txt")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	result := RenderLine(text, fontMap)
	tmpl := template.Must(template.ParseFiles("templates/index.html"))
	tmpl.Execute(w, PageData{Result: result})
}
func main() {
	http.HandleFunc("/", homePage)
	http.HandleFunc("/ascii-art", generate)
	http.ListenAndServe(":8080", nil)
}
