#!/usr/bin/env python3
"""
🎯 منصة المسابقات الرياضية - Streamlit
Math Competition Platform - Streamlit Version
"""

import streamlit as st
import sqlite3
import random
import time
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# إعداد الصفحة
st.set_page_config(
    page_title="منصة المسابقات الرياضية",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# إعداد قاعدة البيانات
def init_database():
    """إنشاء قاعدة البيانات والجداول"""
    conn = sqlite3.connect('math_competition.db')
    cursor = conn.cursor()
    
    # جدول المشاركين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول المسابقات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS competitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant_name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            difficulty INTEGER NOT NULL,
            total_score INTEGER DEFAULT 0,
            questions_data TEXT,
            answers_data TEXT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            is_completed BOOLEAN DEFAULT FALSE
        )
    ''')
    
    conn.commit()
    conn.close()

# مولد الأسئلة
class QuestionGenerator:
    @staticmethod
    def generate_addition_question(difficulty):
        """توليد سؤال جمع"""
        ranges = {
            1: (1, 9), 2: (3, 20), 3: (5, 30),
            4: (9, 40), 5: (21, 99), 6: (25, 99)
        }
        min_val, max_val = ranges.get(difficulty, (1, 9))
        
        num1 = random.randint(min_val, max_val)
        num2 = random.randint(min_val, max_val)
        
        return {
            'question': f"{num1} + {num2}",
            'answer': num1 + num2,
            'operation': 'addition'
        }
    
    @staticmethod
    def generate_subtraction_question(difficulty):
        """توليد سؤال طرح"""
        ranges = {
            1: (1, 9), 2: (3, 20), 3: (5, 30),
            4: (9, 40), 5: (21, 99), 6: (25, 99)
        }
        min_val, max_val = ranges.get(difficulty, (1, 9))
        
        num1 = random.randint(min_val, max_val)
        num2 = random.randint(min_val, max_val)
        
        # التأكد من أن النتيجة موجبة
        larger = max(num1, num2)
        smaller = min(num1, num2)
        
        return {
            'question': f"{larger} - {smaller}",
            'answer': larger - smaller,
            'operation': 'subtraction'
        }
    
    @staticmethod
    def generate_multiplication_question(difficulty):
        """توليد سؤال ضرب"""
        ranges = {
            2: (1, 4), 3: (3, 9), 4: (3, 12),
            5: (7, 15), 6: (8, 15)
        }
        min_val, max_val = ranges.get(difficulty, (1, 4))
        
        num1 = random.randint(min_val, max_val)
        num2 = random.randint(2, 9)
        
        return {
            'question': f"{num1} × {num2}",
            'answer': num1 * num2,
            'operation': 'multiplication'
        }
    
    @staticmethod
    def generate_division_question(difficulty):
        """توليد سؤال قسمة"""
        quotients = [2, 3, 4, 5, 6, 7, 8, 9]
        quotient = random.choice(quotients)
        divisor = random.randint(2, 12)
        dividend = quotient * divisor
        
        return {
            'question': f"{dividend} ÷ {divisor}",
            'answer': quotient,
            'operation': 'division'
        }

# دوال قاعدة البيانات
def save_participant(name, grade):
    """حفظ مشارك جديد"""
    conn = sqlite3.connect('math_competition.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO participants (name, grade) VALUES (?, ?)', (name, grade))
    conn.commit()
    conn.close()

def save_competition(participant_name, grade, difficulty, questions, answers, total_score):
    """حفظ نتائج المسابقة"""
    conn = sqlite3.connect('math_competition.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO competitions 
        (participant_name, grade, difficulty, total_score, questions_data, answers_data, end_time, is_completed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (participant_name, grade, difficulty, total_score, 
          json.dumps(questions), json.dumps(answers), datetime.now(), True))
    conn.commit()
    conn.close()

def get_competitions_data():
    """الحصول على بيانات المسابقات"""
    conn = sqlite3.connect('math_competition.db')
    df = pd.read_sql_query('''
        SELECT participant_name, grade, difficulty, total_score, 
               end_time, questions_data, answers_data
        FROM competitions 
        WHERE is_completed = TRUE
        ORDER BY end_time DESC
    ''', conn)
    conn.close()
    return df

# الواجهة الرئيسية
def main():
    # إنشاء قاعدة البيانات
    init_database()
    
    # العنوان الرئيسي
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0;'>🧮 منصة المسابقات الرياضية</h1>
        <p style='color: white; margin: 0; font-size: 1.2rem;'>Math Competition Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # الشريط الجانبي
    with st.sidebar:
        st.markdown("### 🎯 اختر نوع الدخول")
        user_type = st.radio(
            "نوع المستخدم:",
            ["🎓 تلميذ", "👨‍🏫 معلم"],
            key="user_type"
        )
    
    if user_type == "🎓 تلميذ":
        student_interface()
    else:
        teacher_interface()

def student_interface():
    """واجهة التلاميذ"""
    st.markdown("## 🎓 دخول التلميذ")
    
    # التحقق من رمز الدخول
    if 'access_verified' not in st.session_state:
        st.session_state.access_verified = False
    
    if not st.session_state.access_verified:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔑 أدخل رمز الدخول")
            access_code = st.text_input("رمز الدخول:", type="password", key="access_code")
            
            if st.button("دخول", type="primary", use_container_width=True):
                if access_code == "ben25":
                    st.session_state.access_verified = True
                    st.success("✅ تم التحقق من رمز الدخول!")
                    st.rerun()
                else:
                    st.error("❌ رمز الدخول غير صحيح!")
        return
    
    # إعداد المسابقة
    if 'competition_started' not in st.session_state:
        st.session_state.competition_started = False
    
    if not st.session_state.competition_started:
        setup_competition()
    else:
        run_competition()

def setup_competition():
    """إعداد المسابقة"""
    st.markdown("### 📝 معلومات المشارك")
    
    col1, col2 = st.columns(2)
    
    with col1:
        student_name = st.text_input("اسم التلميذ:", key="student_name")
    
    with col2:
        grade_options = {
            1: "الأول ابتدائي", 2: "الثاني ابتدائي", 3: "الثالث ابتدائي",
            4: "الرابع ابتدائي", 5: "الخامس ابتدائي", 6: "السادس ابتدائي",
            7: "الأول إعدادي", 8: "الثاني إعدادي", 9: "الثالث إعدادي"
        }
        selected_grade = st.selectbox("المستوى الدراسي:", list(grade_options.keys()), 
                                     format_func=lambda x: grade_options[x], key="grade")
    
    st.markdown("### 🎯 اختر مستوى الصعوبة")
    
    difficulty_options = {
        1: "المستوى الأول - سهل جداً",
        2: "المستوى الثاني - سهل",
        3: "المستوى الثالث - متوسط",
        4: "المستوى الرابع - متوسط+",
        5: "المستوى الخامس - صعب",
        6: "المستوى السادس - صعب جداً"
    }
    
    selected_difficulty = st.selectbox("مستوى الصعوبة:", list(difficulty_options.keys()),
                                      format_func=lambda x: difficulty_options[x], key="difficulty")
    
    if st.button("🚀 بدء المسابقة", type="primary", use_container_width=True):
        if student_name:
            st.session_state.student_name = student_name
            st.session_state.grade = selected_grade
            st.session_state.difficulty = selected_difficulty
            st.session_state.competition_started = True
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.questions = []
            st.session_state.answers = []
            st.session_state.start_time = time.time()
            
            # حفظ المشارك
            save_participant(student_name, selected_grade)
            
            st.success(f"✅ مرحباً {student_name}! ستبدأ المسابقة الآن.")
            st.rerun()
        else:
            st.error("❌ يرجى إدخال اسم التلميذ!")

def run_competition():
    """تشغيل المسابقة"""
    total_questions = 15
    
    if st.session_state.current_question >= total_questions:
        show_results()
        return
    
    # عرض التقدم
    progress = st.session_state.current_question / total_questions
    st.progress(progress, text=f"السؤال {st.session_state.current_question + 1} من {total_questions}")
    
    # توليد السؤال
    question_data = generate_question(st.session_state.difficulty)
    
    st.markdown(f"### السؤال {st.session_state.current_question + 1}")
    st.markdown(f"## {question_data['question']} = ؟")
    
    # إدخال الإجابة
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_answer = st.number_input("إجابتك:", value=0, key=f"answer_{st.session_state.current_question}")
        
        if st.button("التالي ➡️", type="primary", use_container_width=True):
            # تحقق من الإجابة
            is_correct = user_answer == question_data['answer']
            if is_correct:
                st.session_state.score += 3
                st.success("✅ إجابة صحيحة!")
            else:
                st.error(f"❌ إجابة خاطئة! الإجابة الصحيحة: {question_data['answer']}")
            
            # حفظ السؤال والإجابة
            st.session_state.questions.append(question_data)
            st.session_state.answers.append({
                'user_answer': user_answer,
                'correct_answer': question_data['answer'],
                'is_correct': is_correct
            })
            
            st.session_state.current_question += 1
            time.sleep(1)
            st.rerun()

def generate_question(difficulty):
    """توليد سؤال حسب المستوى"""
    operations = ['addition', 'subtraction']
    if difficulty >= 2:
        operations.append('multiplication')
    if difficulty >= 3:
        operations.append('division')
    
    operation = random.choice(operations)
    
    if operation == 'addition':
        return QuestionGenerator.generate_addition_question(difficulty)
    elif operation == 'subtraction':
        return QuestionGenerator.generate_subtraction_question(difficulty)
    elif operation == 'multiplication':
        return QuestionGenerator.generate_multiplication_question(difficulty)
    else:
        return QuestionGenerator.generate_division_question(difficulty)

def show_results():
    """عرض النتائج"""
    st.markdown("## 🎉 انتهت المسابقة!")
    
    total_score = st.session_state.score
    total_questions = len(st.session_state.questions)
    percentage = (total_score / (total_questions * 3)) * 100
    
    # حفظ النتائج
    save_competition(
        st.session_state.student_name,
        st.session_state.grade,
        st.session_state.difficulty,
        st.session_state.questions,
        st.session_state.answers,
        total_score
    )
    
    # عرض النتيجة
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("النقاط الإجمالية", f"{total_score} / {total_questions * 3}")
    
    with col2:
        st.metric("النسبة المئوية", f"{percentage:.1f}%")
    
    with col3:
        correct_answers = sum(1 for ans in st.session_state.answers if ans['is_correct'])
        st.metric("الإجابات الصحيحة", f"{correct_answers} / {total_questions}")
    
    # تقييم الأداء
    if percentage >= 90:
        st.success("🌟 ممتاز! أداء رائع!")
    elif percentage >= 75:
        st.success("😊 جيد جداً! استمر!")
    elif percentage >= 60:
        st.info("🙂 جيد! يمكنك التحسن أكثر!")
    else:
        st.warning("😐 تحتاج للمزيد من التدريب!")
    
    if st.button("🔄 مسابقة جديدة", type="primary"):
        # إعادة تعيين الجلسة
        for key in ['competition_started', 'current_question', 'score', 'questions', 'answers']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

def teacher_interface():
    """واجهة المعلمين"""
    st.markdown("## 👨‍🏫 لوحة تحكم المعلم")
    
    # التحقق من كلمة المرور
    if 'teacher_verified' not in st.session_state:
        st.session_state.teacher_verified = False
    
    if not st.session_state.teacher_verified:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 دخول المعلم")
            password = st.text_input("كلمة المرور:", type="password", key="teacher_password")
            
            if st.button("دخول", type="primary", use_container_width=True):
                if password == "teacher123":  # يمكن تغييرها
                    st.session_state.teacher_verified = True
                    st.success("✅ مرحباً بك!")
                    st.rerun()
                else:
                    st.error("❌ كلمة المرور غير صحيحة!")
        return
    
    # لوحة التحكم
    show_dashboard()

def show_dashboard():
    """عرض لوحة التحكم"""
    # الحصول على البيانات
    df = get_competitions_data()
    
    if df.empty:
        st.info("📊 لا توجد مسابقات بعد!")
        return
    
    # إحصائيات عامة
    st.markdown("### 📊 الإحصائيات العامة")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("إجمالي المسابقات", len(df))
    
    with col2:
        st.metric("متوسط النقاط", f"{df['total_score'].mean():.1f}")
    
    with col3:
        st.metric("أعلى نقطة", df['total_score'].max())
    
    with col4:
        unique_participants = df['participant_name'].nunique()
        st.metric("عدد المشاركين", unique_participants)
    
    # الرسوم البيانية
    st.markdown("### 📈 الرسوم البيانية")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # توزيع النقاط
        fig_scores = px.histogram(df, x='total_score', nbins=20, 
                                 title="توزيع النقاط",
                                 labels={'total_score': 'النقاط', 'count': 'العدد'})
        st.plotly_chart(fig_scores, use_container_width=True)
    
    with col2:
        # النقاط حسب المستوى
        avg_by_grade = df.groupby('grade')['total_score'].mean().reset_index()
        fig_grade = px.bar(avg_by_grade, x='grade', y='total_score',
                          title="متوسط النقاط حسب المستوى",
                          labels={'grade': 'المستوى', 'total_score': 'متوسط النقاط'})
        st.plotly_chart(fig_grade, use_container_width=True)
    
    # جدول النتائج
    st.markdown("### 📋 جدول النتائج")
    
    # تنسيق البيانات للعرض
    display_df = df[['participant_name', 'grade', 'difficulty', 'total_score', 'end_time']].copy()
    display_df.columns = ['اسم المشارك', 'المستوى', 'الصعوبة', 'النقاط', 'تاريخ الانتهاء']
    display_df['النسبة المئوية'] = (display_df['النقاط'] / 45 * 100).round(1)
    
    st.dataframe(display_df, use_container_width=True)
    
    # تصدير البيانات
    if st.button("📥 تصدير البيانات (CSV)"):
        csv = display_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="تحميل ملف CSV",
            data=csv,
            file_name=f"نتائج_المسابقات_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
