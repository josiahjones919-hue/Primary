module testbench;

    reg clk;

    CPU cpu_inst (.clk(clk));

    initial begin
        clk = 0;

        //initial val
        cpu_inst.rf.registers[1] = 1; // A
        cpu_inst.rf.registers[2] = 0; // B
        cpu_inst.rf.registers[3] = 1; // C
        cpu_inst.rf.registers[4] = 1; // D

        cpu_inst.rf.registers[15] = 32'hFFFFFFFF;

        #100;

        $display("\n==== FINAL TRACE OUTPUT ====");

        $display("A = %0d", cpu_inst.rf.registers[1]);
        $display("B = %0d", cpu_inst.rf.registers[2]);
        $display("C = %0d", cpu_inst.rf.registers[3]);
        $display("D = %0d", cpu_inst.rf.registers[4]);

        $display("t4 = A & B     = %0d", cpu_inst.rf.registers[12]);
        $display("t6 = ~C & D    = %0d", cpu_inst.rf.registers[14]);
        $display("t0 = FINAL Y   = %0d", cpu_inst.rf.registers[8]);

        $display("EXPECTED Y     = 1");

        #10;
        $finish;
    end

    always #5 clk = ~clk;

endmodule