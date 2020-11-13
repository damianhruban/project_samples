'use strict';

let paths = document.querySelectorAll(".main_roads");
let print_div = document.getElementById("print_div");

//SHOWS NAME OF THE SEGMENT WHEN MOUSE IS ON
function nameOnHover (event) {
	let P=document.createElement("p");
	P.id="print_text";
	P.style.padding="0px 0px";
	P.style.fontSize="1rem";
	P.style.fontWeight="normal";
	let name = "Úsek: " + event.target.dataset.nazev_usek;
	let print = document.createTextNode(name);
	P.appendChild(print);
	print_div.appendChild(P);
	}
function blankOnOut (){			
	print_text.remove();
}
paths.forEach(p => {
	p.addEventListener("mouseover", nameOnHover);
	p.addEventListener("mouseout", blankOnOut);
})

/*SETS UP TIMELINE ANIMATION*/
	let draw = SVG("animation").size(500,500);
	let rect = draw.rect(20, 30);
	let timeline = draw.rect(470, 4);

	function loopYears() {
		for (let x = 0; x < 999; x++) {
			rect.animate(1000, '<>', 1500).move(0, 0);
			rect.animate(1000, '<>', 1500).move(150, 0);
			rect.animate(1000, '<>', 1500).move(300, 0);
			rect.animate(1000, '<>', 1500).move(450, 0);
		}
	}
	loopYears();

//TAKES EXISTING SVG SO IT CAN BE MODIFIED
let mySvg = SVG('map_container').size(800, 800); 
mySvg.svg('<g id="intenzita_brno"></g>');
let myGroup = SVG.get('intenzita_brno');


//BUILDS LEGEND
let legend_border = myGroup.rect(340, 245).attr({ fill: 'white'});

let legend_header = myGroup.text("Průměrný počet průjezdů vozů za 24h").attr({ fill: 'black'}).attr({stroke: 'none'});
legend_header.move(11, 0);
legend_header.font(
	{family:   'Arial Narrow'
	, weight: 'bold'
	, size:     22
	, anchor:   'left'
	, leading:  '2em'
});
let line_legend1 = myGroup.rect(60, 33).attr('fill', 'black').attr('stroke', 'none');
let line_legend2 = myGroup.rect(60, 25).attr('fill', 'black').attr('stroke', 'none');
let line_legend3 = myGroup.rect(60, 18).attr('fill', 'black').attr('stroke', 'none');
let line_legend4 = myGroup.rect(60, 12).attr('fill', 'black').attr('stroke', 'none');
let line_legend5 = myGroup.rect(60, 7).attr('fill', 'black').attr('stroke', 'none');
let line_legend6 = myGroup.rect(60, 3).attr('fill', 'black').attr('stroke', 'none');
line_legend1.animate(1000, '<>', 0).move(190,50);
line_legend2.animate(1000, '<>', 0).move(160,50);
line_legend3.animate(1000, '<>', 0).move(130,50);
line_legend4.animate(1000, '<>', 0).move(100,50);
line_legend5.animate(1000, '<>', 0).move(70, 50);
line_legend6.animate(1000, '<>', 0).move(40, 50);

let leg_num1 = myGroup.text("15 000").attr({ fill: 'black'}).attr({stroke: 'none'});
leg_num1.move(13, 60);
let leg_num2 = myGroup.text("75 000").attr({ fill: 'black'}).attr({stroke: 'none'});
leg_num2.move(220, 90);

let leg_silnice = myGroup.rect(50, 1.5).attr('fill', 'grey').attr('stroke', 'none');
leg_silnice.move(25, 130);
let leg_sil_txt = myGroup.text("komunikace bez dat").attr({ fill: 'black'}).attr({stroke: 'none'});
leg_sil_txt.move(130, 120);

let leg_okres = myGroup.rect(50, 6).attr('fill', 'grey').attr('stroke', 'none');
leg_okres.move(25, 170);
let leg_okr_txt = myGroup.text("hranice města Brna").attr({ fill: 'black'}).attr({stroke: 'none'});
leg_okr_txt.move(130, 160);

let leg_budovy = myGroup.rect(50, 20).attr('fill', 'brown').attr('stroke', 'none');
leg_budovy.move(25, 210);
let leg_bud_txt = myGroup.text("zástavba").attr({ fill: 'black'}).attr({stroke: 'none'});
leg_bud_txt.move(130, 200);



//GETTING DATA FOR EACH YEAR AND ANIMATING PATHS ONE BY ONE
function animateAll() {
	paths.forEach(p => {
		let data00 = p.dataset.int_2000;
		let data05 = p.dataset.int_2005;
		let data10 = p.dataset.int_2010;
		let data16 = p.dataset.int_2016;
		let data_list = [data00, data05, data10, data16]
		for (const data of data_list) {
			let current_id = p.id;			
			let myPath = SVG.get(current_id);
			myPath.animate(1000, '<>', 1500).attr('stroke-width', Math.pow(data, 2)/160000000);
			}
	})
}
//MANUALLY LOOPS TROUGH 4 DIFFERENT PICTURES
function loopAnim() {
	for (let x = 0; x < 999; x++) {
		animateAll();
	}
}
loopAnim();

