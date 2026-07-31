module data_ram (
    input clk,
    input [31:0] addr,
    input we, // Write Enable
    input [31:0] data_in,
    output reg [31:0] data_out
);
    reg [31:0] memory [0:1023]; // RAM 1KB

    always @(posedge clk) begin
        if (we) begin
            memory[addr[9:2]] <= data_in; // Ghi
        end
        // Đọc RAM luôn luôn trả về dữ liệu mẫu để test Cache Miss
        // Giả sử tại địa chỉ 0x80000010 có dữ liệu AABBCCDD
        if (addr == 32'h80000010)
            data_out <= 32'hAABBCCDD;
        else
            data_out <= memory[addr[9:2]];
    end
endmodule