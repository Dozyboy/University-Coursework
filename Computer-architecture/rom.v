module instruction_rom (
    input [31:0] addr,
    output reg [31:0] data_out
);
    always @(*) begin
        // Giả lập nội dung ROM: Nếu đọc địa chỉ 4 thì trả về DEADBEEF
        if (addr == 32'h00000004)
            data_out = 32'hDEADBEEF; // Mã lệnh mẫu
        else
            data_out = 32'h00000000;
    end
endmodule