`timescale 1ns/1ps

module tb_system;
    reg clk;
    reg rst_n;
    reg [31:0] cpu_addr;
    wire [31:0] data_returned;
    wire stall, hit;

    // Gọi module toàn hệ thống ra test
    system_top ut (
        .clk(clk),
        .rst_n(rst_n),
        .cpu_virt_addr(cpu_addr),
        .cpu_data_in(data_returned),
        .stall_cpu(stall),
        .cache_hit(hit)
    );

    // Tạo xung nhịp (Clock)
    always #5 clk = ~clk; // Chu kỳ 10ns

    initial begin
        // Thiết lập file để xem sóng trên GTKWave
        $dumpfile("waveform.vcd");
        $dumpvars(0, tb_system);

        // --- KHỞI TẠO ---
        clk = 0; rst_n = 0; cpu_addr = 0;
        #10 rst_n = 1; // Thả Reset

        // ==========================================
        // KỊCH BẢN 1: Đọc ROM (Địa chỉ thấp)
        // ==========================================
        #20;
        $display("Time %t: [TEST 1] Accessing ROM at 0x00000004", $time);
        cpu_addr = 32'h00000004; 
        // Kỳ vọng: Dữ liệu DEADBEEF trả về. (Cache có thể Miss nhưng vẫn có dữ liệu)
        
        #30; // Chờ một chút

        // ==========================================
        // KỊCH BẢN 2: Đọc RAM (Cache Miss & Refill)
        // ==========================================
        $display("Time %t: [TEST 2] Accessing RAM at 0x80000010 (First Time - MISS)", $time);
        cpu_addr = 32'h80000010; 
        
        // Logic mô phỏng:
        // 1. Cache check -> Miss (hit=0)
        // 2. Stall -> lên 1
        // 3. Đọc RAM -> trả về AABBCCDD
        // 4. Stall -> xuống 0
        
        wait(stall == 0); // Chờ cho đến khi hết Stall (Refill xong)
        #10;

        // ==========================================
        // KỊCH BẢN 3: Đọc RAM (Cache Hit)
        // ==========================================
        $display("Time %t: [TEST 3] Accessing RAM at 0x80000010 (Second Time - HIT)", $time);
        // Giữ nguyên địa chỉ cũ, chỉ cần quan sát tín hiệu
        #10;
        
        // Kết thúc mô phỏng
        #50 $finish;
    end
endmodule