module Control (
    input [5:0] func,
    output reg ALUOp,
    output reg InvB,
    output reg RegWrite
);

    always @(*) begin

        ALUOp = 0;
        InvB = 0;
        RegWrite = 1;

        case (func)

            6'b000000: begin // AND
                ALUOp = 0;
                InvB = 0;
            end

            6'b000001: begin // OR
                ALUOp = 1;
                InvB = 0;
            end

            6'b000010: begin // AND-NOT
                ALUOp = 0;
                InvB = 1;
            end

            default: begin
                ALUOp = 0;
                InvB = 0;
                RegWrite = 0;
            end

        endcase
    end

endmodule