module top (
    input clk,
    input rst
);

`define ROM_ADDR_BITS 8
`define RAM_ADDR_BITS 8

initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, top);
end

//
// Signal Declarations
//

wire [3:0] cnt;

wire rst_n;

wire        rv_mem_valid;       // memory access output from cpu
wire [31:0] rv_mem_addr;        // memory address output from cpu
wire        rv_mem_instr;       // output from cpu indicating instruction fetch

wire [31:0] rv_mem_wdata;       // data bus output from cpu
wire [ 3:0] rv_mem_byte_wr_ena; // byte write-enable output from cpu

reg  [31:0] rv_mem_rdata;       // data bus input to cpu
reg         rv_mem_ready;       // input to cpu indicating rdata is valid

wire [15:0] rv_mem_addr_upper;

wire        rom_mem_ready;      // acknowledge output from ROM
wire [31:0] rom_mem_rdata;      // data output from rom block

wire        ram_mem_ready;      // acknowledge output from RAM
wire [31:0] ram_mem_rdata;      // data output from ram block

wire        per_mem_ready;      // acknowledge output from periph
wire [31:0] per_mem_rdata;      // data output from periph

wire addr_sel_rom; // address select for ROM
wire addr_sel_ram; // address select for RAM
wire addr_sel_per; // address select for periph

//
// Static assignments
//

assign rst_n = ~rst;
assign rv_mem_addr_upper = rv_mem_addr[31:16];

//
// Address Decoder
//

/*
    Memory map (so far):

    0x1000_0000 -> ROM
    0x2000_0000 -> RAM

    Top 16 bits are used for selecting subsystem access.
*/

assign addr_sel_rom = rv_mem_valid ? (rv_mem_addr_upper == 16'h1000) : 1'b0;
assign addr_sel_ram = rv_mem_valid ? (rv_mem_addr_upper == 16'h2000) : 1'b0;
assign addr_sel_per = rv_mem_valid ? (rv_mem_addr_upper == 16'h4000) : 1'b0;

always @(*) begin

    // Default assignments
    rv_mem_rdata = 32'b0;
    rv_mem_ready = 1'b0;

    // ROM selector
    if (addr_sel_rom) begin
        rv_mem_rdata = rom_mem_rdata;
        rv_mem_ready = rom_mem_ready;
    end

    // RAM selector
    if (addr_sel_ram) begin
        rv_mem_rdata = ram_mem_rdata;
        rv_mem_ready = ram_mem_ready;
    end

    // periph selector
    if (addr_sel_per) begin
        rv_mem_rdata = per_mem_rdata;
        rv_mem_ready = per_mem_ready;
    end
end

assign per_mem_ready = 1'b1; // just acknowledge all periph writes for now

//
// Submodules
//

picorv32 #(
    .PROGADDR_RESET(32'h 1000_0000),
    .PROGADDR_IRQ(32'h 1000_0010),
    .COMPRESSED_ISA(1)
) cpu (
    .clk(clk),
    .resetn(rst_n),
    .trap(rv_trap),

    .mem_valid(rv_mem_valid),
    .mem_addr(rv_mem_addr),
    .mem_wdata(rv_mem_wdata),
    .mem_wstrb(rv_mem_byte_wr_ena),
    .mem_instr(rv_mem_instr),
    .mem_ready(rv_mem_ready),
    .mem_rdata(rv_mem_rdata),

    // ignoring mem_la interface
    .mem_la_read(),
    .mem_la_write(),
    .mem_la_addr(),
    .mem_la_wdata(),
    .mem_la_wstrb(),

    // ignoring pcpi
    .pcpi_valid(),
    .pcpi_insn(),
    .pcpi_rs1(),
    .pcpi_rs2(),
    .pcpi_wr(1'b0),
    .pcpi_rd(32'b0),
    .pcpi_wait(1'b0),
    .pcpi_ready(1'b0),

    // ignoring irq
    .irq(32'b0),
    .eoi(),

    // ignoring trace
    .trace_valid(),
    .trace_data()
);

rv_rom32 #(
    .ADDR_BITS(`ROM_ADDR_BITS)
) rom (
    .clk(clk),
    .addr_valid(addr_sel_rom),
    .addr(rv_mem_addr[`ROM_ADDR_BITS - 1 : 0]),
    .data_valid(rom_mem_ready),
    .data(rom_mem_rdata)
);

rv_ram32_sync #(
    .ADDR_BITS(`RAM_ADDR_BITS)
) ram (
    .clk(clk),
    .addr_valid(addr_sel_ram),
    .addr(rv_mem_addr[`RAM_ADDR_BITS - 1 : 0]),
    .ack(ram_mem_ready),
    .wdata(rv_mem_wdata),
    .wr_en(rv_mem_byte_wr_ena),
    .rdata(ram_mem_rdata)
);

endmodule // top
