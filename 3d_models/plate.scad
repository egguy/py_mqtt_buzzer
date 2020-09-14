$fn=100;
diam_button = 58;
wall_thickness = 2;
screw_diam = 3;
offset = 1;

plate = diam_button * 2;

module base_top_plate() {
difference(){
    square(plate);
    translate([plate/2, plate/2, 0]){
        circle(diam_button/2);
    }
}
}


module top_plate(){
    hole_diameter = screw_diam / 2;
    move = wall_thickness+hole_diameter+offset;
    difference(){
        base_top_plate();
        translate([move, move, 0]){
            circle(hole_diameter);
        }
        translate([move, plate-move, 0]){
            circle(hole_diameter);
        }
        translate([plate-move, move, 0]){
            circle(hole_diameter);
        }
        translate([plate-move, plate-move, 0]){
            circle(hole_diameter);
        }
    }
}

linear_extrude(2){
    top_plate();
}