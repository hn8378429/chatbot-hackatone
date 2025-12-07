import type { ReactNode } from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import { useState } from 'react';

type FeatureItem = {
  title: string;
  icon: string;
  description: string;
  gradient: string;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'AI-Powered Learning',
    icon: '🤖',
    description: 'Intelligent content adaptation based on your experience level and learning patterns',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  },
  {
    title: 'Personalized Content',
    icon: '🎯',
    description: 'Tailored explanations and examples that match your background and goals',
    gradient: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
  },
  {
    title: 'Bilingual Assistant',
    icon: '🌐',
    description: 'Get explanations in both English and Urdu with intelligent translation',
    gradient: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
  },
  {
    title: 'Interactive Chat',
    icon: '💬',
    description: 'Real-time Q&A with context-aware responses from book content',
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
  },
  {
    title: 'Code Examples',
    icon: '💻',
    description: 'Practical coding examples adapted to your programming language preference',
    gradient: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
  },
  {
    title: 'Progress Tracking',
    icon: '📊',
    description: 'Monitor your learning journey with personalized insights and recommendations',
    gradient: 'linear-gradient(135deg, #06b6d4 0%, #0ea5e9 100%)',
  },
];

function Feature({ title, icon, description, gradient }: FeatureItem) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div 
      className={clsx('col col--4')}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className={styles.featureCard}>
        <div 
          className={styles.featureIcon}
          style={{ background: gradient }}
        >
          <span className={styles.icon}>{icon}</span>
        </div>
        <div className={styles.featureContent}>
          <Heading as="h3" className={styles.featureTitle}>
            {title}
          </Heading>
          <p className={styles.featureDescription}>{description}</p>
        </div>
        <div className={`${styles.featureGlow} ${isHovered ? styles.glowActive : ''}`} 
             style={{ background: gradient }} />
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.featuresSection}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>
            <span className="gradient-text">Why Choose Our Platform?</span>
          </h2>
          <p className={styles.sectionSubtitle}>
            Experience the future of personalized learning with AI-powered features
          </p>
        </div>
        
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
        
        <div className={styles.ctaSection}>
          <div className={styles.ctaCard}>
            <div className={styles.ctaContent}>
              <h3>Ready to Start Learning?</h3>
              <p>Join thousands of learners who are mastering concepts with AI assistance</p>
              <div className={styles.ctaButtons}>
                <button className="button button--primary button--lg">
                  Get Started Free
                </button>
                <button className="button button--outline button--lg">
                  View Demo
                </button>
              </div>
            </div>
            <div className={styles.ctaIllustration}>
              <div className={styles.floatingElements}>
                <span className={styles.float1}>🚀</span>
                <span className={styles.float2}>📚</span>
                <span className={styles.float3}>💡</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}