module CPU (
    input clk
);

    reg [31:0] PC = 0;

    wire [31:0] instruction;
    wire [4:0] rs, rt, rd;
    wire [5:0] func;

    wire [31:0] readData1, readData2;
    wire [31:0] alu_out;

    wire ALUOp, InvB, RegWrite;

    reg [31:0] t4, t6;

    assign rs = instruction[25:21];
    assign rt = instruction[20:16];
    assign rd = instruction[15:11];
    assign func = instruction[5:0];

    InstructionMemory imem (
        .addr(PC),
        .instruction(instruction)
    );

    Control ctrl (
        .func(func),
        .ALUOp(ALUOp),
        .InvB(InvB),
        .RegWrite(RegWrite)
    );

    RegFile rf (
        .clk(clk),
        .RegWrite(RegWrite),
        .rs(rs),
        .rt(rt),
        .rd(rd),
        .WriteData(alu_out),
        .ReadData1(readData1),
        .ReadData2(readData2)
    );

    ALU alu (
        .A(readData1),
        .B(readData2),
        .ALUOp(ALUOp),
        .InvB(InvB),
        .Result(alu_out)
    );

    always @(*) begin
        t4 = rf.registers[1] & rf.registers[2];
        t6 = (~rf.registers[3]) & rf.registers[4];
    end

    always @(posedge clk) begin

        $display("\n--- INSTRUCTION @ PC=%0d ---", PC);
        $display("func=%b ALUOp=%b InvB=%b RegWrite=%b", func, ALUOp, InvB, RegWrite);
        $display("rs=%0d rt=%0d rd=%0d", rs, rt, rd);

        if (func == 6'b000000 && InvB == 0)
            $display("OP: AND");
        else if (func == 6'b000001)
            $display("OP: OR");
        else if (func == 6'b000010)
            $display("OP: AND-NOT");

        if (RegWrite)
            $display("WRITE: r%0d = %d", rd, alu_out);

        PC <= PC + 1;
    end

endmodule