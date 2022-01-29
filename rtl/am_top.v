
module am_top(rst, clk);

input rst;
input clk;

top top(.rst(rst), .clk(clk));

initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, top);
end

endmodule
