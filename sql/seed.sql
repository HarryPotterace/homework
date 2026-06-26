USE mental_health_system;

INSERT INTO admins (username, name, role, contact, password_hash) VALUES
('consultant', '陈老师', 'consultant', 'chen@example.com', 'scrypt:32768:8:1$3NRUUHJagnXZDbGi$5839306caad2a320ce59389f26f877d3d59ae8a8d52aae315206f9dbbeadb12fcb52adf96c9349ff65bc4df4ae9b9d3b05f08b83fdd5a8e121209d05bbcbde53'),
('admin', '系统管理员', 'admin', 'admin@example.com', 'scrypt:32768:8:1$Td2VMGzmbIgdeMUM$097747d7116345639de11056479f7047e250bf2f8603aa59edc8140b14138a56f1df7ccb640cacbc38182c0947c52548bc742bec76f31175bac375dd488a550e');

INSERT INTO scales (code, name, description) VALUES
('PHQ-9', 'PHQ-9 抑郁量表', '用于初步筛查近期抑郁情绪倾向。'),
('GAD-7', 'GAD-7 焦虑量表', '用于初步筛查近期焦虑情绪倾向。');

INSERT INTO scale_questions (scale_code, question_order, content) VALUES
('PHQ-9', 1, '做事时提不起劲或没有兴趣'),
('PHQ-9', 2, '感到心情低落、沮丧或绝望'),
('PHQ-9', 3, '入睡困难、睡不安稳或睡眠过多'),
('PHQ-9', 4, '感到疲倦或没有活力'),
('PHQ-9', 5, '食欲不振或吃太多'),
('PHQ-9', 6, '觉得自己很糟，或觉得自己很失败'),
('PHQ-9', 7, '注意力不集中'),
('PHQ-9', 8, '动作或说话变得迟缓，或恰恰相反变得烦躁'),
('PHQ-9', 9, '有过伤害自己或觉得不如消失的念头'),
('GAD-7', 1, '感到紧张、焦虑或心神不宁'),
('GAD-7', 2, '无法停止担忧或控制担忧'),
('GAD-7', 3, '对各种事情都过度担心'),
('GAD-7', 4, '很难放松下来'),
('GAD-7', 5, '因为坐立不安而难以安静坐着'),
('GAD-7', 6, '变得容易烦躁或急躁'),
('GAD-7', 7, '感到好像将有可怕的事情发生');

INSERT INTO counselors_schedule (counselor_name, title, schedule_date, slot, is_available) VALUES
('陈老师', '国家二级心理咨询师', '2026-07-01', '09:00-10:00', TRUE),
('李老师', '高校心理中心咨询师', '2026-07-01', '15:00-16:00', TRUE),
('王老师', '学院专职辅导员', '2026-07-02', '10:00-11:00', TRUE);
