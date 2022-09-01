$fn=30;
diam_button = 58;
wall_thickness = 2;
screw_diam = 3;
offset = 1;
heigth = 75;

support_lenght = 30;

plate = diam_button * 2;

/*
module support() {
    linear_extrude(heigth){
        translate([support_lenght/2, 0]){
            square([wall_thickness, support_lenght]);
            translate([support_lenght/2,support_lenght/2, 0]){
                rotate(90){
                    square([wall_thickness, support_lenght]);
                }
            }
    
    }
}

}
*/
module support() {
    linear_extrude(heigth){
        translate([support_lenght/2, support_lenght/2]){
            difference(){
                circle(support_lenght/2);
                circle((support_lenght/2)-1);
            }
        }
    }
}

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
    move = wall_thickness/2+(hole_diameter+offset)/2+offset;
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

margin = 1;

// 1 st Bottome Left
translate([
    wall_thickness+margin,
    wall_thickness+margin
]){
    support();
}

// 2nd - Bottom Right
translate([
    plate-wall_thickness-support_lenght-margin,
    wall_thickness+margin
]){
    support();
}

// 3rd Up Left
translate([
    wall_thickness+margin,
    plate-wall_thickness-support_lenght-margin
]){
    support();
}

// Up right
translate([
    plate-wall_thickness-support_lenght-margin,
    plate-wall_thickness-support_lenght-margin
]){
    support();
}
