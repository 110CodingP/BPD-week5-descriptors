import { readFileSync } from "fs";

describe('Evaluate Submission', () => {
    let balance: string;

    beforeAll(() => {
        balance = readFileSync('out.txt', 'utf8').trim();
    });

    it('should be defined', () => {
        expect(balance).toBeDefined();
    });

    it('should be correct balance', () => {
        expect(balance).toBe('777.62402534');
    });
});