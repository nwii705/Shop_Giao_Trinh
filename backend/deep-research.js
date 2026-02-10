/**
 * Deep Research Agent - Bộ não nghiên cứu sâu cho SKKN/KHBD
 * 
 * Sử dụng Perplexity Sonar qua OpenRouter để tìm kiếm và tổng hợp thông tin
 * Model perplexity/sonar tự động search internet và trả về kết quả tổng hợp
 * 
 * Quy trình:
 * 1. Nhận đề tài từ user
 * 2. Gọi Perplexity Sonar để tìm kiếm real-time
 * 3. Tổng hợp thành báo cáo nghiên cứu tiền khả thi
 * 
 * Chỉ cần 1 API key: OpenRouter API Key
 */

const https = require('https');

class DeepResearchAgent {
    constructor(openRouterKey, tavilyKey = null) {
        // OpenRouter key dùng cho cả Perplexity Sonar và Gemini
        this.openRouterKey = openRouterKey;
        this.tavilyKey = tavilyKey; // Giữ lại cho fallback (optional)
        this.logs = [];
        
        // Model cho Deep Research (Perplexity Sonar - có khả năng search internet)
        this.searchModel = 'perplexity/sonar';
        // Model cho tổng hợp (Gemini)
        this.synthesisModel = 'google/gemini-2.5-flash';
    }

    log(message) {
        const timestamp = new Date().toISOString();
        this.logs.push({ timestamp, message });
        console.log(`[DeepResearch] ${message}`);
    }

    /**
     * Gọi OpenRouter API (hỗ trợ nhiều model)
     */
    async callOpenRouter(model, prompt, temperature = 0.7, maxTokens = 8000) {
        return new Promise((resolve, reject) => {
            const postData = JSON.stringify({
                model: model,
                messages: [
                    { role: 'user', content: prompt }
                ],
                max_tokens: maxTokens,
                temperature: temperature
            });

            const options = {
                hostname: 'openrouter.ai',
                path: '/api/v1/chat/completions',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.openRouterKey}`,
                    'HTTP-Referer': 'http://localhost:5000',
                    'X-Title': 'EduAI Deep Research'
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
            req.setTimeout(180000, () => { // 3 phút timeout cho deep research
                req.destroy();
                reject(new Error('OpenRouter request timeout (3 minutes)'));
            });

            req.write(postData);
            req.end();
        });
    }

    /**
     * Tìm kiếm với Perplexity Sonar qua OpenRouter
     * Model này tự động search internet và trả về kết quả tổng hợp
     */
    async searchWithPerplexity(topic, role, subject, level) {
        this.log(`🔍 Đang tìm kiếm với Perplexity Sonar: "${topic}"`);
        
        const currentYear = new Date().getFullYear();
        
        const searchPrompt = `Bạn là chuyên gia nghiên cứu giáo dục Việt Nam. 

Nhiệm vụ: Tìm kiếm và tổng hợp thông tin THỰC TẾ từ internet cho đề tài SKKN sau:

=== THÔNG TIN ĐỀ TÀI ===
• Tên đề tài: "${topic}"
• Vị trí tác giả: ${role}
• Lĩnh vực: ${subject}
• Cấp học: ${level}

=== YÊU CẦU TÌM KIẾM (năm ${currentYear - 2}-${currentYear}) ===

Hãy tìm kiếm và tổng hợp các thông tin sau:

1. **VĂN BẢN PHÁP LÝ MỚI NHẤT**:
   - Các Nghị quyết, Thông tư, Công văn của Bộ GD&ĐT liên quan
   - Chương trình GDPT 2018 và các văn bản hướng dẫn
   - Văn bản về chuyển đổi số, đổi mới phương pháp dạy học
   - Ghi rõ số hiệu, ngày ban hành

2. **SỐ LIỆU THỐNG KÊ THỰC TẾ**:
   - Tỷ lệ áp dụng các phương pháp/công nghệ mới trong giáo dục
   - Số liệu về hiệu quả các mô hình đổi mới
   - Thống kê từ Bộ GD&ĐT, các Sở GD&ĐT, nghiên cứu khoa học
   - Ghi rõ nguồn và năm thống kê

3. **CÁC MÔ HÌNH THÀNH CÔNG**:
   - 2-3 trường hợp áp dụng thành công tại Việt Nam
   - Kết quả cụ thể đạt được
   - Bài học kinh nghiệm

4. **XU HƯỚNG VÀ THÁCH THỨC**:
   - Xu hướng mới trong lĩnh vực ${subject}
   - Thách thức thực tế tại các trường ${level}
   - Cơ hội phát triển

5. **TÀI LIỆU THAM KHẢO**:
   - Sách, giáo trình liên quan
   - Bài báo khoa học, nghiên cứu
   - Link tham khảo (nếu có)

=== ĐỊNH DẠNG OUTPUT ===
Viết báo cáo tổng hợp khoảng 1500-2000 từ, chia theo các mục trên.
Mỗi thông tin phải ghi rõ NGUỒN TRÍCH DẪN (tên văn bản, năm, website...).
Nếu không tìm thấy thông tin cụ thể, ghi chú "Cần xác minh thêm".`;

        try {
            const result = await this.callOpenRouter(
                this.searchModel, 
                searchPrompt, 
                0.4, // Temperature thấp cho search chính xác
                6000
            );
            this.log(`✅ Perplexity Sonar đã hoàn thành tìm kiếm`);
            return result;
        } catch (error) {
            this.log(`⚠️ Lỗi Perplexity Sonar: ${error.message}`);
            throw error;
        }
    }

    /**
     * Fallback: Tìm kiếm với Tavily API (nếu có key)
     */
    async searchWithTavily(query) {
        if (!this.tavilyKey) {
            return [];
        }

        this.log(`🔍 Fallback Tavily: "${query}"`);

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
                    "thuvienphapluat.vn"
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
                            resolve(result.results.map(r => ({
                                title: r.title,
                                url: r.url,
                                content: r.content
                            })));
                        } else {
                            resolve([]);
                        }
                    } catch (e) {
                        resolve([]);
                    }
                });
            });

            req.on('error', () => resolve([]));
            req.setTimeout(10000, () => {
                req.destroy();
                resolve([]);
            });

            req.write(postData);
            req.end();
        });
    }

    /**
     * Tổng hợp kết quả thành Báo cáo Nghiên cứu Tiền Khả Thi
     */
    async synthesizeReport(topic, role, subject, level, perplexityData, tavilyData = []) {
        this.log('📝 Đang tổng hợp báo cáo cuối cùng...');

        // Gom thêm dữ liệu từ Tavily nếu có
        const additionalContext = tavilyData.length > 0 
            ? `\n\n=== DỮ LIỆU BỔ SUNG TỪ TAVILY ===\n${tavilyData.map((r, i) => 
                `[${i + 1}] ${r.title}\nURL: ${r.url}\nNội dung: ${r.content}`
            ).join('\n\n')}`
            : '';

        const synthesisPrompt = `Bạn là Trợ lý Nghiên cứu Giáo dục cấp cao tại Việt Nam.

=== THÔNG TIN ĐỀ TÀI SKKN ===
• Tên đề tài: "${topic}"
• Vị trí tác giả: ${role}
• Lĩnh vực: ${subject}
• Cấp học: ${level}

=== KẾT QUẢ TỪ DEEP RESEARCH (Perplexity Sonar) ===
${perplexityData}
${additionalContext}

=== NHIỆM VỤ ===
Dựa trên dữ liệu nghiên cứu ở trên, hãy viết một "BÁO CÁO NGHIÊN CỨU TIỀN KHẢ THI" hoàn chỉnh, được định dạng như sau:

## 1. CƠ SỞ PHÁP LÝ
- Liệt kê các văn bản, nghị quyết, thông tư MỚI NHẤT liên quan
- Ghi rõ số hiệu văn bản, năm ban hành
- Ví dụ: Nghị quyết 29-NQ/TW (2013), Thông tư 32/2018/TT-BGDĐT, Công văn 5512/BGDĐT-GDTrH...

## 2. CƠ SỞ THỰC TIỄN & SỐ LIỆU
- Tổng hợp số liệu thống kê về thực trạng vấn đề
- Các khó khăn, thách thức đang tồn tại
- Xu hướng phát triển hiện nay
- GHI RÕ NGUỒN cho mỗi số liệu

## 3. CÁC MÔ HÌNH THÀNH CÔNG
- Giới thiệu 2-3 mô hình/case study đã áp dụng thành công
- Phân tích điểm mạnh, điểm yếu
- Bài học kinh nghiệm rút ra

## 4. GỢI Ý GIẢI PHÁP "MỚI & SÁNG TẠO"
Dựa trên nghiên cứu, gợi ý 4-5 giải pháp có tính MỚI cho đề tài:
| STT | Tên giải pháp | Mô tả ngắn | Tính mới | Điều kiện thực hiện |
|-----|---------------|------------|----------|---------------------|
| 1   | ...           | ...        | ...      | ...                 |
| 2   | ...           | ...        | ...      | ...                 |
| ... | ...           | ...        | ...      | ...                 |

## 5. TÀI LIỆU THAM KHẢO GỢI Ý
Liệt kê 8-10 tài liệu theo format trích dẫn khoa học:
1. Tác giả (Năm). Tên tài liệu. Nhà xuất bản/Website.
2. ...

=== YÊU CẦU ===
✓ Viết đầy đủ 1500-2000 từ
✓ Văn phong học thuật, dễ hiểu
✓ Trích dẫn nguồn rõ ràng
✓ Số liệu phù hợp thực tế giáo dục Việt Nam
✓ Giải pháp phù hợp với vai trò ${role} và cấp học ${level}`;

        try {
            const report = await this.callOpenRouter(
                this.synthesisModel,
                synthesisPrompt,
                0.6,
                8000
            );
            this.log('✅ Hoàn thành báo cáo nghiên cứu!');
            return report;
        } catch (e) {
            this.log(`❌ Lỗi tổng hợp: ${e.message}`);
            throw e;
        }
    }

    /**
     * MAIN: Thực hiện toàn bộ quy trình Deep Research
     * Sử dụng Perplexity Sonar làm công cụ search chính
     */
    async performDeepResearch(topic, role, subject, level) {
        this.logs = [];
        
        const startTime = Date.now();
        this.log(`🚀 BẮT ĐẦU DEEP RESEARCH (Powered by Perplexity Sonar)`);
        this.log(`📌 Đề tài: "${topic}"`);
        this.log(`👤 Vai trò: ${role}`);
        this.log(`📚 Lĩnh vực: ${subject}`);
        this.log(`🏫 Cấp học: ${level}`);

        try {
            // Bước 1: Tìm kiếm với Perplexity Sonar (real-time internet search)
            this.log('🔎 Bước 1: Tìm kiếm với Perplexity Sonar...');
            const perplexityData = await this.searchWithPerplexity(topic, role, subject, level);
            
            // Bước 2 (Optional): Bổ sung với Tavily nếu có key
            let tavilyData = [];
            if (this.tavilyKey) {
                this.log('🔎 Bước 2: Bổ sung với Tavily...');
                const queries = [
                    `${topic} văn bản pháp luật ${new Date().getFullYear()}`,
                    `${topic} số liệu thống kê giáo dục Việt Nam`
                ];
                for (const query of queries) {
                    const results = await this.searchWithTavily(query);
                    tavilyData.push(...results);
                    await new Promise(r => setTimeout(r, 500));
                }
                this.log(`  ✓ Tavily bổ sung ${tavilyData.length} nguồn`);
            }

            // Bước 3: Tổng hợp thành báo cáo cuối cùng
            this.log('📝 Bước 3: Tổng hợp báo cáo cuối cùng với Gemini...');
            const report = await this.synthesizeReport(
                topic, role, subject, level,
                perplexityData,
                tavilyData
            );

            const duration = ((Date.now() - startTime) / 1000).toFixed(1);
            this.log(`⏱️ Hoàn thành trong ${duration}s`);

            // Extract sources từ báo cáo (nếu có thể)
            const sources = tavilyData.map(r => ({
                title: r.title,
                url: r.url
            }));

            return {
                success: true,
                topic,
                role,
                subject,
                level,
                report,
                sources,
                searchEngine: 'Perplexity Sonar + Gemini 2.5 Flash',
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
