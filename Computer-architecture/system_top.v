`include "rom.v"
`include "ram.v"
`include "cache.v"
`include "tlb.v"

module system_top (
    input clk,
    input rst_n,
    input [31:0] cpu_virt_addr, // CPU chỉ đưa ra địa chỉ ảo
    output [31:0] cpu_data_in,
    output stall_cpu,
    output cache_hit
);

    // Dây nối nội bộ
    wire [31:0] phys_addr;
    wire tlb_hit;
    
    wire [31:0] rom_out, ram_out, cache_out;
    wire ram_read_req;
    
    // 1. TLB: Dịch địa chỉ
    tlb u_tlb (
        .virt_addr(cpu_virt_addr), 
        .phys_addr(phys_addr), 
        .hit(tlb_hit)
    );

    // 2. Address Decoder (Logic chọn ROM hay RAM)
    reg [31:0] memory_bus_data;
    // Nếu bit cao nhất là 0 -> ROM. Nếu là 1 -> RAM
    wire is_rom = (phys_addr[31] == 1'b0);
    
    // 3. ROM
    instruction_rom u_rom (.addr(phys_addr), .data_out(rom_out));

    // 4. RAM
    data_ram u_ram (
        .clk(clk), .addr(phys_addr), .we(1'b0), 
        .data_in(32'b0), .data_out(ram_out)
    );

    // Logic Mux chọn dữ liệu nạp vào Cache
    always @(*) begin
        if (is_rom) memory_bus_data = rom_out;
        else        memory_bus_data = ram_out;
    end

    // 5. Cache L1
    cache_l1 u_cache (
        .clk(clk), .rst_n(rst_n),
        .addr(phys_addr),
        .ram_data(memory_bus_data), // Nối vào bus chung
        .cpu_data(cpu_data_in),
        .hit(cache_hit),
        .stall(stall_cpu),
        .ram_read(ram_read_req)
    );

endmodule