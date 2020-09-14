$fn=100;
diam_button = 58;

plate = diam_button * 2;
heigth = 75;
wall_thickness =  2;
screw_hole_diam = 3;

module keystone(){
    rotate([0,-90,-90]){
        cube([20,15,wall_thickness]);
    }
}

module box(){
    inside_box = plate - wall_thickness;
    translate([plate/2, plate/2, heigth/2]){
    difference(){
        cube([plate, plate, heigth], center=true);
        translate([0, 0, wall_thickness/2]){
        cube([inside_box, inside_box, heigth-wall_thickness], center=true);
        }
    }
}
}

module screw_hole(diam, offset=1){
    center = diam + offset;
    difference(){
        square(center);
        translate([center/2, center/2, 0]){
            circle(diam/2);
        }
    }
}

module screw_3d(){
    linear_extrude(heigth){
        screw_hole(screw_hole_diam);
    }
}




difference(){
    box();
    translate([(plate-15)/2, 0, 5]){
        keystone();
    }
}

wall_trans = wall_thickness/2;
move = screw_hole_diam+1;

translate([wall_trans, wall_trans, 0]){
    screw_3d();
}
translate([plate-wall_trans-move, wall_trans, 0]){
    screw_3d();
}
translate([wall_trans, plate-wall_trans-move, 0]){
    screw_3d();
}
translate([plate-wall_trans-move, plate-wall_trans-move, 0]){
    screw_3d();
}