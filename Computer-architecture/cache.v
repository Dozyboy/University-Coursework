module cache_l1 (
    input clk,
    input rst_n,
    input [31:0] addr,      // Địa chỉ từ CPU
    input [31:0] ram_data,  // Dữ liệu từ RAM (để nạp vào Cache)
    output reg [31:0] cpu_data, // Dữ liệu trả về CPU
    output reg hit,         // Báo Hit cho CPU
    output reg stall,       // Báo Stall (dừng) cho CPU
    output reg ram_read     // Lệnh đọc RAM
);

    // Cấu trúc Cache: 64 dòng (Lines)
    reg [31:0] data_mem [0:63];
    reg [23:0] tag_mem  [0:63];
    reg        valid_mem[0:63];

    // Tách địa chỉ: Tag (24 bit) - Index (6 bit) - Offset (2 bit)
    wire [5:0] index = addr[7:2];
    wire [23:0] tag  = addr[31:8];

    // Máy trạng thái (FSM)
    parameter IDLE = 0, ALLOCATE = 1;
    reg state;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= IDLE;
            hit <= 0; stall <= 0; ram_read <= 0;
            // Reset toàn bộ Valid bit (lặp thủ công hoặc dùng loop trong testbench)
             valid_mem[index] <= 0; 
        end else begin
            case (state)
                IDLE: begin
                    // Kiểm tra: Valid = 1 VÀ Tag khớp
                    if (valid_mem[index] && (tag_mem[index] == tag)) begin
                        // --- CACHE HIT ---
                        hit <= 1;
                        stall <= 0;
                        cpu_data <= data_mem[index];
                        ram_read <= 0;
                    end else begin
                        // --- CACHE MISS ---
                        hit <= 0;
                        stall <= 1; // Yêu cầu CPU dừng
                        ram_read <= 1; // Yêu cầu đọc RAM
                        state <= ALLOCATE; // Chuyển trạng thái
                    end
                end

                ALLOCATE: begin
                    // --- REFILL CACHE ---
                    // Giả lập RAM đã trả dữ liệu về (ram_data)
                    data_mem[index] <= ram_data; // Ghi dữ liệu vào Cache
                    tag_mem[index]  <= tag;      // Cập nhật Tag
                    valid_mem[index]<= 1;        // Đánh dấu Valid
                    
                    stall <= 0; // Hết Stall
                    state <= IDLE; // Quay về kiểm tra lại
                end
            endcase
        end
    end
endmodule