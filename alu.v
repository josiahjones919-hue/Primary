module ALU (
    input [31:0] A,
    input [31:0] B,
    input ALUOp,
    input InvB,
    output reg [31:0] Result
);

    wire [31:0] B_in;

    assign B_in = InvB ? ~B : B;

    always @(*) begin
        case (ALUOp)
            1'b0: Result = A & B_in; // AND / AND-NOT
            1'b1: Result = A | B_in; // OR
            default: Result = 32'b0;
        endcase
    end

endmodule