using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;

namespace PuzzleNamespace {
    class Puzzle {
        static List<int> instrArr = new List<int>();
        static List<int> oparr    = new List<int>();
        static List<bool> executed = new List<bool>(instrArr.Count());
        static int accum, pc;

        static Tuple<int, int> parseLine(string line)
        {
            string[] splitted = line.Split(' ');
            char[] chararr = splitted[1].ToCharArray();
            if (chararr[0] == '+') chararr[0] = '0';
            switch (splitted[0]) {
            case "nop": return new Tuple<int, int>(0, int.Parse(chararr));
            case "acc": return new Tuple<int, int>(1, int.Parse(chararr));
            case "jmp": return new Tuple<int, int>(2, int.Parse(chararr));
            default: return null;
            }
        }
        
        static void exec(int op)
        {
            Console.WriteLine("{0} {1} accum: {2} pc: {3}", disass(instrArr[pc]), instrArr[pc+1], accum, pc);
            executed[pc] = executed[pc+1] = true;
            switch (op) {
            case 0: pc+=2; break;
            case 1: accum += instrArr[pc+1]; pc+=2; break;
            case 2: pc += instrArr[pc+1]*2; break;
            }
        }

        static void Main(string[] args)
        {
            File.ReadAllLines("input8.txt").ToList().Select(line => parseLine(line)).ToList().ForEach(t => {
                    executed.Add(false); executed.Add(false);
                    instrArr.Add(t.Item1); instrArr.Add(t.Item2); });
            while (!executed[pc])
                exec(instrArr[pc]);
            Console.WriteLine(accum);
        }

        static string disass(int instr)
        {
            switch(instr) {
            case 0: return "nop";
            case 1: return "acc";
            case 2: return "jmp";
            default: return null;
            }
        }
    }
}
