"use strict";
let serverUrl = "http://localhost:5000";

let handleSearch = (e) => {
  console.log("Hi");
  e.preventDefault();
  let searchParams = {
    query: document.getElementsByClassName("input")[0].value,
  };
  let url = new URL(serverUrl + "/api/search-results");
  url.search = new URLSearchParams(searchParams).toString();
  fetch(url)
    .then((res) => {
      if (res.ok) {
        // Change search bar position
        let changeInitStyle = Array.from(
          document.getElementsByClassName("init")
        );
        for (let element of changeInitStyle) {
          element.classList.remove("init");
        }
      }
      return res.json();
    })
    .then((data) => {
      // Clear previous results
      document.getElementsByClassName("search-results-container")[0].innerHTML =
        "";
      if (data.length == 0) {
        document.getElementsByClassName(
          "search-results-container"
        )[0].innerHTML = "<h2>No Results</h2>";
      } else {
        document.getElementsByClassName(
          "search-results-container"
        )[0].innerHTML = `Found ${data.length} similar DNA sequence(s) :<hr/>`;
        data.forEach((result) => {
          let resultItem = document.createElement("div");
          let title = result[0];
          let contents = result[1];
          resultItem.innerHTML = `<a href="#"><h2>📂 ${title}</h2></a><p class="summary">${contents}</p><hr/>`;
          document
            .getElementsByClassName("search-results-container")[0]
            .appendChild(resultItem);
        });
      }
    });
};

document
  .getElementsByClassName("search-form")[0]
  .addEventListener("submit", handleSearch);

document.getElementById("submit").addEventListener("click", handleSearch);
