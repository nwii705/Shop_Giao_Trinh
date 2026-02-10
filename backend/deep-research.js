/**
 * Deep Research Agent - Bộ não nghiên cứu sâu cho SKKN/KHBD
 * 
 * Quy trình 3 bước:
 * 1. PLAN - Phân tích đề tài, lên kế hoạch tìm kiếm
 * 2. SEARCH - Tìm kiếm đa chiều (Pháp lý, Lý luận, Thực tiễn)
 * 3. SYNTHESIZE - Đọc hiểu và tổng hợp thành báo cáo
 * 
 * Sử dụng:
 * - Tavily API: Tìm kiếm web tối ưu cho AI (1000 lượt free/tháng)
 * - Gemini 1.5 Flash: Đọc và tổng hợp (context 1M tokens)
 */

const https = require('https');
const http = require('http');

class DeepResearchAgent {
    constructor(geminiKey, tavilyKey) {
        this.geminiKey = geminiKey;
        this.tavilyKey = tavilyKey;
        this.searchResults = [];
        this.logs = [];
    }

    log(message) {
        const timestamp = new Date().toISOString();
        this.logs.push({ timestamp, message });
        console.log(`[DeepResearch] ${message}`);
    }

    /**
     * BƯỚC 1: Lên kế hoạch tìm kiếm
     * AI tự sinh ra các từ khóa chuyên sâu từ đề tài
     */
    async planSearchQueries(topic, role, subject, level) {
        this.log(`📋 Đang lên kế hoạch nghiên cứu cho: "${topic}"`);
        
        const planPrompt = `Bạn là chuyên gia nghiên cứu giáo dục Việt Nam.
        
Đề tài SKKN: "${topic}"
Vị trí tác giả: ${role}
Lĩnh vực: ${subject}
Cấp học: ${level}

Nhiệm vụ: Hãy sinh ra 6 từ khóa/câu truy vấn TÌM KIẾM GOOGLE bằng tiếng Việt để tìm thông tin cho đề tài này.

Yêu cầu từ khóa bao gồm:
1. Văn bản pháp lý mới nhất (Nghị quyết, Thông tư, Công văn)
2. Số liệu thống kê về thực trạng
3. Các mô hình/giải pháp thành công
4. Nghiên cứu khoa học liên quan
5. Xu hướng mới trong lĩnh vực này
6. Case study thực tế tại Việt Nam

Trả lời ĐÚNG ĐỊNH DẠNG JSON:
{
  "queries": [
    "từ khóa 1",
    "từ khóa 2",
    "từ khóa 3",
    "từ khóa 4",
    "từ khóa 5",
    "từ khóa 6"
  ]
}`;

        try {
            const response = await this.callGemini(planPrompt, 0.3);
            // Parse JSON từ response
            const jsonMatch = response.match(/\{[\s\S]*\}/);
            if (jsonMatch) {
                const parsed = JSON.parse(jsonMatch[0]);
                this.log(`✅ Đã tạo ${parsed.queries.length} từ khóa tìm kiếm`);
                return parsed.queries;
            }
        } catch (e) {
            this.log(`⚠️ Lỗi tạo kế hoạch: ${e.message}`);
        }

        // Fallback: Tự tạo từ khóa mặc định
        return [
            `${topic} văn bản chỉ đạo ${new Date().getFullYear()}`,
            `thực trạng ${topic} trường học Việt Nam`,
            `số liệu thống kê ${subject} ${level}`,
            `giải pháp ${topic} hiệu quả`,
            `mô hình ${topic} thành công`,
            `nghiên cứu khoa học về ${topic}`
        ];
    }

    /**
     * BƯỚC 2: Thực thi tìm kiếm với Tavily API
     */
    async searchWithTavily(query) {
        if (!this.tavilyKey) {
            this.log('⚠️ Không có Tavily API Key, bỏ qua tìm kiếm');
            return [];
        }

        this.log(`🔍 Tìm kiếm: "${query}"`);

        return new Promise((resolve) => {
            const postData = JSON.stringify({
                api_key: this.tavilyKey,
                query: query,
                search_depth: "advanced",
                include_answer: true,
                include_raw_content: false,
                max_results: 5,
                include_domains: [
                    "moet.gov.vn",
                    "giaoduc.net.vn",
                    "vnexpress.net",
                    "tuoitre.vn",
                    "thanhnien.vn",
                    "baochinhphu.vn",
                    "dangcongsan.vn",
                    "thuvienphapluat.vn",
                    "luatvietnam.vn"
                ]
            });

            const options = {
                hostname: 'api.tavily.com',
                path: '/search',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(postData)
                }
            };

            const req = https.request(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(data);
                        if (result.results) {
                            this.log(`  ✓ Tìm thấy ${result.results.length} kết quả`);
                            resolve(result.results.map(r => ({
                                title: r.title,
                                url: r.url,
                                content: r.content,
                                score: r.score
                            })));
                        } else {
                            resolve([]);
                        }
                    } catch (e) {
                        this.log(`  ✗ Lỗi parse: ${e.message}`);
                        resolve([]);
                    }
                });
            });

            req.on('error', (e) => {
                this.log(`  ✗ Lỗi request: ${e.message}`);
                resolve([]);
            });

            req.setTimeout(10000, () => {
                req.destroy();
                resolve([]);
            });

            req.write(postData);
            req.end();
        });
    }

    /**
     * Fallback: Sử dụng Google Custom Search API (nếu có)
     */
    async searchWithGoogle(query, googleApiKey, googleCx) {
        if (!googleApiKey || !googleCx) {
            return [];
        }

        this.log(`🔍 Google Search: "${query}"`);

        return new Promise((resolve) => {
            const encodedQuery = encodeURIComponent(query);
            const url = `https://www.googleapis.com/customsearch/v1?key=${googleApiKey}&cx=${googleCx}&q=${encodedQuery}&num=5`;

            https.get(url, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(data);
                        if (result.items) {
                            resolve(result.items.map(item => ({
                                title: item.title,
                                url: item.link,
                                content: item.snippet,
                                score: 0.8
                            })));
                        } else {
                            resolve([]);
                        }
                    } catch (e) {
                        resolve([]);
                    }
                });
            }).on('error', () => resolve([]));
        });
    }

    /**
     * Gọi Gemini API qua OpenRouter
     */
    async callGemini(prompt, temperature = 0.7) {
        return new Promise((resolve, reject) => {
            const postData = JSON.stringify({
                model: 'google/gemini-2.5-flash',
                messages: [
                    { role: 'user', content: prompt }
                ],
                max_tokens: 8000,
                temperature: temperature
            });

            const options = {
                hostname: 'openrouter.ai',
                path: '/api/v1/chat/completions',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.geminiKey}`,
                    'HTTP-Referer': 'http://localhost:5000',
                    'X-Title': 'EduAI Generator'
                }
            };

            const req = https.request(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(data);
                        if (result.choices && result.choices[0]) {
                            resolve(result.choices[0].message.content);
                        } else if (result.error) {
                            reject(new Error(result.error.message || JSON.stringify(result.error)));
                        } else {
                            reject(new Error('No response from OpenRouter: ' + JSON.stringify(result)));
                        }
                    } catch (e) {
                        reject(e);
                    }
                });
            });

            req.on('error', reject);
            req.setTimeout(120000, () => {
                req.destroy();
                reject(new Error('OpenRouter request timeout'));
            });

            req.write(postData);
            req.end();
        });
    }

    /**
     * BƯỚC 3: Tổng hợp kết quả thành Báo cáo Nghiên cứu
     */
    async synthesizeReport(topic, role, subject, level, searchResults) {
        this.log('📝 Đang tổng hợp báo cáo nghiên cứu...');

        // Gom tất cả nội dung tìm được
        const researchContext = searchResults.map((r, i) => 
            `[Nguồn ${i + 1}] ${r.title}\nURL: ${r.url}\nNội dung: ${r.content}`
        ).join('\n\n---\n\n');

        const synthesisPrompt = `Bạn là Trợ lý Nghiên cứu Giáo dục cấp cao tại Việt Nam.

=== THÔNG TIN ĐỀ TÀI ===
• Tên đề tài SKKN: "${topic}"
• Vị trí tác giả: ${role}
• Lĩnh vực: ${subject}
• Cấp học: ${level}

=== DỮ LIỆU THÔ TỪ INTERNET (Deep Research) ===
${researchContext || 'Không tìm thấy dữ liệu từ internet. Hãy sử dụng kiến thức có sẵn.'}

=== NHIỆM VỤ ===
Dựa trên các dữ liệu trên, hãy viết một "BÁO CÁO NGHIÊN CỨU TIỀN KHẢ THI" (khoảng 1500-2000 từ) gồm các phần sau:

## 1. CƠ SỞ PHÁP LÝ
- Liệt kê các văn bản, nghị quyết, thông tư mới nhất liên quan đến đề tài
- Trích dẫn chính xác số hiệu, năm ban hành
- Ví dụ: Nghị quyết 29-NQ/TW (2013), Thông tư 32/2018/TT-BGDĐT, CV 5512/BGDĐT-GDTrH...

## 2. CƠ SỞ THỰC TIỄN & SỐ LIỆU
- Tổng hợp các con số thống kê về thực trạng vấn đề
- Các khó khăn, thách thức đang tồn tại
- Xu hướng phát triển trong lĩnh vực này
- Nếu có số liệu từ nguồn, hãy trích dẫn. Nếu không, tạo số liệu hợp lý có chú thích "Số liệu ước tính"

## 3. CÁC MÔ HÌNH THÀNH CÔNG
- Giới thiệu 2-3 mô hình/case study đã thành công trong lĩnh vực này
- Phân tích điểm mạnh, điểm yếu của từng mô hình
- Bài học kinh nghiệm rút ra

## 4. GỢI Ý GIẢI PHÁP "MỚI & SÁNG TẠO"
Dựa trên nghiên cứu, gợi ý 4-5 giải pháp có tính MỚI cho đề tài, mỗi giải pháp gồm:
- Tên giải pháp
- Mô tả ngắn gọn (2-3 câu)
- Tính mới/sáng tạo
- Điều kiện thực hiện

## 5. TÀI LIỆU THAM KHẢO GỢI Ý
- Liệt kê 8-10 tài liệu nên đọc thêm (sách, bài báo, văn bản pháp quy)
- Đúng format trích dẫn khoa học

=== YÊU CẦU ===
✓ Viết bằng tiếng Việt, văn phong học thuật
✓ Trung thực, khách quan, có trích dẫn nguồn khi có thể
✓ Số liệu phải hợp lý với thực tế giáo dục Việt Nam
✓ Giải pháp phải phù hợp với vai trò ${role} và cấp học ${level}`;

        try {
            const report = await this.callGemini(synthesisPrompt, 0.6);
            this.log('✅ Hoàn thành báo cáo nghiên cứu!');
            return report;
        } catch (e) {
            this.log(`❌ Lỗi tổng hợp: ${e.message}`);
            throw e;
        }
    }

    /**
     * MAIN: Thực hiện toàn bộ quy trình Deep Research
     */
    async performDeepResearch(topic, role, subject, level) {
        this.logs = [];
        this.searchResults = [];
        
        const startTime = Date.now();
        this.log(`🚀 BẮT ĐẦU DEEP RESEARCH`);
        this.log(`📌 Đề tài: "${topic}"`);
        this.log(`👤 Vai trò: ${role}`);
        this.log(`📚 Lĩnh vực: ${subject}`);
        this.log(`🏫 Cấp học: ${level}`);

        try {
            // Bước 1: Lên kế hoạch
            const queries = await this.planSearchQueries(topic, role, subject, level);
            
            // Bước 2: Tìm kiếm
            this.log('🔎 Bắt đầu tìm kiếm đa chiều...');
            for (const query of queries) {
                const results = await this.searchWithTavily(query);
                this.searchResults.push(...results);
                // Delay để tránh rate limit
                await new Promise(r => setTimeout(r, 500));
            }
            
            // Loại bỏ trùng lặp theo URL
            const uniqueResults = [];
            const seenUrls = new Set();
            for (const r of this.searchResults) {
                if (!seenUrls.has(r.url)) {
                    seenUrls.add(r.url);
                    uniqueResults.push(r);
                }
            }
            this.searchResults = uniqueResults;
            this.log(`📊 Tổng cộng: ${this.searchResults.length} nguồn thông tin duy nhất`);

            // Bước 3: Tổng hợp
            const report = await this.synthesizeReport(
                topic, role, subject, level, 
                this.searchResults.slice(0, 20) // Giới hạn 20 nguồn
            );

            const duration = ((Date.now() - startTime) / 1000).toFixed(1);
            this.log(`⏱️ Hoàn thành trong ${duration}s`);

            return {
                success: true,
                topic,
                role,
                subject,
                level,
                report,
                sources: this.searchResults.slice(0, 20).map(r => ({
                    title: r.title,
                    url: r.url
                })),
                logs: this.logs,
                duration: parseFloat(duration)
            };

        } catch (error) {
            this.log(`❌ Lỗi: ${error.message}`);
            return {
                success: false,
                error: error.message,
                logs: this.logs
            };
        }
    }
}

module.exports = DeepResearchAgent;
