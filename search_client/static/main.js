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
      document.getElementsByClassName("search-results-container")[0].innerHTML = "";
      let qry=searchParams["query"].toString();
      let count=0;
      if(qry.length>=9)
      {
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
            if(contents.toString().length>=9)
            {
              count++;
              document
              .getElementsByClassName("search-results-container")[0]
              .appendChild(resultItem);
            }
          });
        }
      } else {
        document.getElementsByClassName(
          "search-results-container"
        )[0].innerHTML = "<h2>Invalid Query. Enter a query of length greater than 9</h2>";
      }
      if(count==0)
      {
        document.getElementsByClassName(
          "search-results-container"
        )[0].innerHTML = "<h2>No Results</h2>";
      }
    });
};

document
  .getElementsByClassName("search-form")[0]
  .addEventListener("submit", handleSearch);

document.getElementById("submit").addEventListener("click", handleSearch);
