//script.js
// d3
// .json("data/nobel_winners_cleaned.json")
// .then((data) => {
//   d3
//   .select("h2#data-title").
//   text("All the Nobel-winners");
//   d3
//   .select("div#data pre")
//   .html(JSON
//     .stringify(data, null, 4)
//   );
// });

// delivering the chinks of data obtained
// after a pd.groupby operation
let loadCountryWinnersJSON = function (country) {
  d3.json("data/winners_by_country/" + country + ".json")
  .then(function(data) {
    d3.select("h2#data-tile").text(
      "All the Nobel-winners from " + country
    );

    d3.select("div#data pre").html(
      JSON.stringify(data, null, 4)
    );
  })

  .catch((error) => console.log(error));
}