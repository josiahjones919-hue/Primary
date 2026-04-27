module RegFile (
    input clk,
    input RegWrite,
    input [4:0] rs,
    input [4:0] rt,
    input [4:0] rd,
    input [31:0] WriteData,
    output [31:0] ReadData1,
    output [31:0] ReadData2
);

    reg [31:0] registers [0:31];

    integer i; 

    initial begin
        for (i = 0; i < 32; i = i + 1)
            registers[i] = 0;
    end

    assign ReadData1 = registers[rs];
    assign ReadData2 = registers[rt];

    always @(posedge clk) begin
        if (RegWrite)
            registers[rd] <= WriteData;
    end

endmodule