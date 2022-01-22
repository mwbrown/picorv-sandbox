
// This define controls whether the ROM acts like a true asynchronous ROM,
// or if it uses registered output (compatible with an FPGA RAM block)
`define ROM_ASYNC

// 32-bit ROM module for the PicoRV32. Defaults to 1kiB (256 addresses)
module rv_rom32 #(
    parameter ADDR_BITS = 8
) (
    input clk,
    input addr_valid,
    input [ADDR_BITS - 1 : 0] addr,
    output reg data_valid,
    output [31:0] data
);

reg [31:0] data_async;
reg [31:0] rom_data [1 << ADDR_BITS - 1 : 0];

// Asynchronous data read
assign data_async = addr_valid ? rom_data[addr >> 2] : {32{1'b0}};

`ifdef ROM_ASYNC

assign data = data_async;
assign data_valid = addr_valid;

`else 

reg [31:0] data_sync;

// Use a DFF on the data output.
always @(posedge clk) begin
    if (addr_valid) begin
        data_sync <= data_async;
    end

    data_valid <= addr_valid;
end

assign data = data_sync;

`endif

endmodule // rv_rom32

//
// Synchronous RAM
//

module rv_ram32_sync #(
    parameter ADDR_BITS = 8
) (
    input clk,
    input addr_valid,
    input [ADDR_BITS - 1 : 0] addr,
    output reg ack,
    input [31:0] wdata,
    input [3:0] wr_en,
    output reg [31:0] rdata
);

wire write;

reg [31:0] ram_data [1 << ADDR_BITS - 1 : 0];

// Create a wired-OR of all the byte enables.
assign write = |wr_en;

always @(posedge clk) begin
    // TBD: This logic only works if addr_valid doesn't stay high for
    //      long enough for this RAM to reassert the ack signal. It is
    //      assumed the PicoRV32 brings the mem_valid signal low on the
    //      next clock cycle.
    if (addr_valid && ~ack) begin
        if (write) begin
            rdata <= 32'bx;

            if (wr_en[3]) ram_data[addr >> 2][31:24] <= wdata[31:24]; 
            if (wr_en[2]) ram_data[addr >> 2][23:16] <= wdata[23:16];
            if (wr_en[1]) ram_data[addr >> 2][15: 8] <= wdata[15: 8];
            if (wr_en[0]) ram_data[addr >> 2][ 7: 0] <= wdata[ 7: 0];

        end
        else begin
            rdata <= ram_data[addr >> 2];
        end
        ack <= 1'b1;
    end
    else begin
        ack <= 1'b0;
    end
end

endmodule // rv_ram32