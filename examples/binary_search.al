var a = input;
var min = 1;
var max = 1000000;
var b = 50;
repeat 100 {
    if (a == b) {
        print Ready \n;
    }
    if (a != b) {
        if (b < a) {
            var max = b;
            print min \n;
            print max \n;
        }
        if (b > a) {
            var min = b;
            print min \n;
            print max \n;
        }
        add b max min \n;
        div b b 2;
    }
}

