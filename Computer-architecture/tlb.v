module tlb (
    input [31:0] virt_addr,
    output [31:0] phys_addr,
    output hit
);
    // Trong demo này, TLB ánh xạ 1:1 (Direct Map) để đơn giản
    assign phys_addr = virt_addr; 
    assign hit = 1'b1; // Luôn luôn Hit
endmodule