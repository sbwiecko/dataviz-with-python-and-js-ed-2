// npm install d3
// add `"type": "module"` in package.json
// finally run `node test_d3.js`

import * as d3 from 'd3';

//var color_scal = d3.interpolate() //doesn't work
var color_scal = d3.scaleLinear()
.domain([-1, 0, 1])
.range(["red", "green", "blue"]);

console.log(color_scal(.5)); // rgb(0, 64, 128)

var oScale = d3.scaleBand()
               .domain([1,2,3,4,5])
               .rangeRound([0,400]);

console.log(oScale(3));
console.log(oScale(3.5)); // undefined