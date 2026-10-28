import random

class IterativeCode:
    def __init__(self, k1, k2, parity_groups):
        self.k1 = k1
        self.k2 = k2
        self.k = k1 * k2
        self.parity_groups = sorted(set(parity_groups))
        self.r = 0
        self.build_parity_structure()
    
    def build_parity_structure(self):
        self.h_parities = self.k1
        self.v_parities = self.k2
        self.r = self.h_parities + self.v_parities
        self.d1_parities = 0
        self.d2_parities = 0
        self.hv_parity = False
        if 3 in self.parity_groups:
            self.d1_parities = self.k1 + self.k2 - 1
            self.r += self.d1_parities
        if 4 in self.parity_groups:
            self.d2_parities = self.k1 + self.k2 - 1
            self.r += self.d2_parities
        if 5 in self.parity_groups:
            self.r += 1
            self.hv_parity = True
        self.n = self.k + self.r
    
    def encode(self, bits):
        if len(bits) != self.k:
            raise ValueError("Length mismatch")
        matrix = [[int(bits[i * self.k2 + j]) for j in range(self.k2)] for i in range(self.k1)]
        codeword = list(bits[:])
        
        h_parities = []
        for i in range(self.k1):
            p = sum(matrix[i][j] for j in range(self.k2)) % 2
            h_parities.append(p)
            codeword.append(p)
        
        v_parities = []
        for j in range(self.k2):
            p = sum(matrix[i][j] for i in range(self.k1)) % 2
            v_parities.append(p)
            codeword.append(p)
        
        if self.d1_parities:
            d1_parities = [0] * self.d1_parities
            for i in range(self.k1):
                for j in range(self.k2):
                    if matrix[i][j]:
                        d1_parities[i + j] ^= 1
            for p in d1_parities:
                codeword.append(p)
        
        if self.d2_parities:
            d2_parities = [0] * self.d2_parities
            for i in range(self.k1):
                for j in range(self.k2):
                    if matrix[i][j]:
                        d2_parities[(self.k1 - 1 - i) + j] ^= 1
            for p in d2_parities:
                codeword.append(p)
        
        if self.hv_parity:
            hv = sum(bits) % 2
            hv ^= sum(h_parities) % 2
            hv ^= sum(v_parities) % 2
            if self.d1_parities:
                hv ^= sum(d1_parities) % 2
            if self.d2_parities:
                hv ^= sum(d2_parities) % 2
            codeword.append(hv)
        
        return codeword
    
    def decode(self, codeword):
        if len(codeword) != self.n:
            raise ValueError("Length mismatch")
        bits_info = codeword[:self.k]
        matrix = [[int(bits_info[i * self.k2 + j]) for j in range(self.k2)] for i in range(self.k1)]
        
        pos = self.k
        h_received = list(codeword[pos:pos + self.h_parities])
        pos += self.h_parities
        v_received = list(codeword[pos:pos + self.v_parities])
        pos += self.v_parities
        
        if self.d1_parities:
            pos += self.d1_parities
        if self.d2_parities:
            pos += self.d2_parities
        
        h_calc = [sum(matrix[i][j] for j in range(self.k2)) % 2 for i in range(self.k1)]
        v_calc = [sum(matrix[i][j] for i in range(self.k1)) % 2 for j in range(self.k2)]
        
        h_errors = [h_calc[i] != h_received[i] for i in range(self.h_parities)]
        v_errors = [v_calc[j] != v_received[j] for j in range(self.v_parities)]
        
        corrected = bits_info[:]
        
        if all(not h for h in h_errors) and all(not v for v in v_errors):
            return corrected, 0
        if any(h_errors) and any(v_errors):
            for i in range(self.k1):
                if h_errors[i]:
                    for j in range(self.k2):
                        if v_errors[j]:
                            idx = i * self.k2 + j
                            corrected[idx] ^= 1
                            return corrected, 1
            return corrected, 0
        if any(h_errors):
            for i in range(self.k1):
                if h_errors[i]:
                    for j in range(self.k2):
                        corrected[i * self.k2 + j] ^= 1
            return corrected, self.k2
        if any(v_errors):
            for j in range(self.k2):
                if v_errors[j]:
                    for i in range(self.k1):
                        corrected[i * self.k2 + j] ^= 1
            return corrected, self.k1
        
        return corrected, 0
    
    def add_errors(self, codeword, num_errors):
        result = codeword[:]
        positions = random.sample(range(len(codeword)), min(num_errors, len(codeword)))
        for p in positions:
            result[p] ^= 1
        return result, positions
