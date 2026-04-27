module InstructionMemory (
    input [31:0] addr,
    output [31:0] instruction
);

    reg [31:0] memory [0:31];

    initial begin
        
        memory[0] = {6'b000000, 5'd1, 5'd2, 5'd12, 6'b000000};

        
        memory[1] = {6'b000000, 5'd15, 5'd3, 5'd13, 6'b000010};

        
        memory[2] = {6'b000000, 5'd13, 5'd4, 5'd14, 6'b000000};

        
        memory[3] = {6'b000000, 5'd12, 5'd14, 5'd8, 6'b000001};
    end

    assign instruction = memory[addr];

endmodule