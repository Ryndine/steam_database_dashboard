///// Code based on D3 as well as article by Nadieh Bremer at https://bl.ocks.org/nbremer/d2720fdaab1123df73f4806360a09c9e ////

function onPageLoad() {
	var margin = {left:30, top:30, right:30, bottom:30},
		width = Math.min(window.innerWidth, 300) - margin.left - margin.right,
		height = Math.min(window.innerWidth, 300) - margin.top - margin.bottom,
		innerRadius = Math.min(width, height) * .39,
		outerRadius = innerRadius * 1.1;

	var Genres = ["RPG","ACT","RAC","ADV","STR","IND","F2P",'SIM',"CAS","SPO","MMO","EA"];
	colors = ['#00065b', '#440a56', '#671852', '#85294d', '#a13e49', '#b95444', '#cf6d3f', '#e28639', '#f1a231', '#fcc027', '#ffdf18', '#ffff00']
		
	const matrix = [
		[0,91,76,90,92,89,38,81,83,74,31,34],
		[91,0,85,94,90,91,38,83,88,83,28,35],
		[76,85,0,86,84,81,33,88,89,92,31,45],
		[90,94,86,0,89,94,32,84,93,85,23,36],
		[92,90,84,89,0,90,35,92,88,81,27,37],
		[89,91,81,94,90,0,36,79,92,81,19,32],
		[38,38,33,32,35,36,0,30,31,35,57,17],
		[81,83,88,84,92,79,30,0,86,83,33,46],
		[83,88,89,93,88,92,31,86,0,89,24,39],
		[74,83,92,85,81,81,35,83,89,0,26,41],
		[31,28,31,23,27,19,57,33,24,26,0,16],
		[34,35,45,36,37,32,17,46,39,41,16,0]
	];

	////////////////////////////////////////////////////////////
	/////////// Create scale and layout functions //////////////
	////////////////////////////////////////////////////////////

	var colors = d3.scaleOrdinal()
		.domain(d3.range(Genres.length))
		.range(colors);

	var chord = customChordLayout()
		.padding(.15)
		.sortChords(d3.descending)
		.matrix(matrix);
			
	var arc = d3.arc()
		.innerRadius(innerRadius*1.01)
		.outerRadius(outerRadius);

	var path = d3.ribbon()
		.radius(innerRadius);
		
	////////////////////////////////////////////////////////////
	////////////////////// Create SVG //////////////////////////
	////////////////////////////////////////////////////////////

	console.log("holder", document.getElementById('chordchart'));
		
	var svg = d3.select("#chordchart").append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
		.attr("transform", "translate(" + (width/2 + margin.left) + "," + (height/2 + margin.top) + ")");

	////////////////////////////////////////////////////////////
	/////////////// Create the gradient fills //////////////////
	////////////////////////////////////////////////////////////

	//Function to create the unique id for each chord gradient
	function getGradID(d){ return "linkGrad-" + d.source.index + "-" + d.target.index; }

	//Create the gradients definitions for each chord
	var grads = svg.append("defs").selectAll("linearGradient")
		.data(chord.chords())
	.enter().append("linearGradient")
		//Create the unique ID for this specific source-target pairing
		.attr("id", getGradID)
		.attr("gradientUnits", "userSpaceOnUse")
		//Find the location where the source chord starts
		.attr("x1", function(d,i) { return innerRadius * Math.cos((d.source.endAngle-d.source.startAngle)/2 + d.source.startAngle - Math.PI/2); })
		.attr("y1", function(d,i) { return innerRadius * Math.sin((d.source.endAngle-d.source.startAngle)/2 + d.source.startAngle - Math.PI/2); })
		//Find the location where the target chord starts 
		.attr("x2", function(d,i) { return innerRadius * Math.cos((d.target.endAngle-d.target.startAngle)/2 + d.target.startAngle - Math.PI/2); })
		.attr("y2", function(d,i) { return innerRadius * Math.sin((d.target.endAngle-d.target.startAngle)/2 + d.target.startAngle - Math.PI/2); })

	//Set the starting color (at 0%)
	grads.append("stop")
		.attr("offset", "0%")
		.attr("stop-color", function(d){ return colors(d.source.index); });

	//Set the ending color (at 100%)
	grads.append("stop")
		.attr("offset", "100%")
		.attr("stop-color", function(d){ return colors(d.target.index); });
			
	////////////////////////////////////////////////////////////
	////////////////// Draw outer Arcs /////////////////////////
	////////////////////////////////////////////////////////////

	var outerArcs = svg.selectAll("g.group")
		.data(chord.groups)
		.enter().append("g")
		.attr("class", "group")
		.on("mouseover", fade(.1))
		.on("mouseout", fade());

	outerArcs.append("path")
		.style("fill", function(d) { return colors(d.index); })
		.attr("d", arc);
		
	////////////////////////////////////////////////////////////
	////////////////////// Append Names ////////////////////////
	////////////////////////////////////////////////////////////

	//Append the label names on the outside
	outerArcs.append("text")
	.each(function(d) { d.angle = (d.startAngle + d.endAngle) / 2; })
	.attr("dy", "0.05em")
	.attr("class", "titles")
	.attr("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null; })
	.attr("transform", function(d) {
			return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
			+ "translate(" + (outerRadius + 10) + ")"
			+ (d.angle > Math.PI ? "rotate(180)" : "");
	})
	.text(function(d,i) { return Genres[i]; });
		
	////////////////////////////////////////////////////////////
	////////////////// Draw inner chords ///////////////////////
	////////////////////////////////////////////////////////////
	
	svg.selectAll("path.chord")
		.data(chord.chords)
		.enter().append("path")
		.attr("class", "chord")
		.style("fill", function(d){ return "url(#" + getGradID(d) + ")"; })
		.style("fill-opacity", 0.8)
		.attr("d", path);

	////////////////////////////////////////////////////////////
	////////////////// Extra Functions /////////////////////////
	////////////////////////////////////////////////////////////

	//Returns an event handler for fading a given chord group.
	function fade(opacity) {
	return function(d,i) {
		svg.selectAll("path.chord")
			.filter(function(d) { return d.source.index != i && d.target.index != i; })
			.transition()
			.style("opacity", opacity);
	};
	}//fade

	function customChordLayout() {
		var ε = 1e-6, ε2 = ε * ε, π = Math.PI, τ = 2 * π, τε = τ - ε, halfπ = π / 2, d3_radians = π / 180, d3_degrees = 180 / π;
		var chord = {}, chords, groups, matrix, n, padding = 0, sortGroups, sortSubgroups, sortChords;
		function relayout() {
			var subgroups = {}, groupSums = [], groupIndex = d3.range(n), subgroupIndex = [], k, x, x0, i, j;
			var numSeq;
			chords = [];
			groups = [];
			k = 0, i = -1;
			
			while (++i < n) {
				x = 0, j = -1, numSeq = [];
				while (++j < n) {
				x += matrix[i][j];
				}
				groupSums.push(x);
				//////////////////////////////////////
				////////////// New part //////////////
				//////////////////////////////////////
				for(var m = 0; m < n; m++) {	
					numSeq[m] = (n+(i-1)-m)%n;
				}
				subgroupIndex.push(numSeq);
				//////////////////////////////////////
				//////////  End new part /////////////
				//////////////////////////////////////
				k += x;
			}//while
		
			k = (τ - padding * n) / k;
			x = 0, i = -1;
			while (++i < n) {
				x0 = x, j = -1;
				while (++j < n) {
					var di = groupIndex[i], dj = subgroupIndex[di][j], v = matrix[di][dj], a0 = x, a1 = x += v * k;
					subgroups[di + "-" + dj] = {
						index: di,
						subindex: dj,
						startAngle: a0,
						endAngle: a1,
						value: v
					};
				}//while
				
				groups[di] = {
					index: di,
					startAngle: x0,
					endAngle: x,
					value: (x - x0) / k
				};
				x += padding;
			}//while

			i = -1;
			while (++i < n) {
				j = i - 1;
				while (++j < n) {
					var source = subgroups[i + "-" + j], target = subgroups[j + "-" + i];
					if (source.value || target.value) {
						chords.push(source.value < target.value ? {
							source: target,
							target: source
						} : {
							source: source,
							target: target
						});
					}//if
				}//while
			}//while
		if (sortChords) resort();
		}//function relayout
		
		function resort() {
		chords.sort(function(a, b) {
			return sortChords((a.source.value + a.target.value) / 2, (b.source.value + b.target.value) / 2);
		});
		}
		chord.matrix = function(x) {
		if (!arguments.length) return matrix;
		n = (matrix = x) && matrix.length;
		chords = groups = null;
		return chord;
		};
		chord.padding = function(x) {
		if (!arguments.length) return padding;
		padding = x;
		chords = groups = null;
		return chord;
		};
		chord.sortGroups = function(x) {
		if (!arguments.length) return sortGroups;
		sortGroups = x;
		chords = groups = null;
		return chord;
		};
		chord.sortSubgroups = function(x) {
		if (!arguments.length) return sortSubgroups;
		sortSubgroups = x;
		chords = null;
		return chord;
		};
		chord.sortChords = function(x) {
		if (!arguments.length) return sortChords;
		sortChords = x;
		if (chords) resort();
		return chord;
		};
		chord.chords = function() {
		if (!chords) relayout();
		return chords;
		};
		chord.groups = function() {
		if (!groups) relayout();
		return groups;
		};
		return chord;
	};
}

let intervalId = setInterval(() => {
	if (document.getElementById('chordchart') == null) {
		return;
	}
	clearInterval(intervalId);
	onPageLoad();
}, 100)
