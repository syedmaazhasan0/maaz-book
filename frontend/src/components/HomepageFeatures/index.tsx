import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Comprehensive Coverage',
    Svg: require('@site/static/img/robot_perception.svg').default,
    description: (
      <>
        Explore 11 comprehensive chapters covering Physical AI fundamentals, perception systems,
        locomotion, manipulation, learning algorithms, and real-world applications.
      </>
    ),
  },
  {
    title: 'Interactive Learning',
    Svg: require('@site/static/img/robot_learning.svg').default,
    description: (
      <>
        Ask our AI-powered chatbot questions about humanoid robotics, robot platforms like Atlas and ASIMO,
        and get instant answers from the book content.
      </>
    ),
  },
  {
    title: 'Cutting-Edge Topics',
    Svg: require('@site/static/img/robot_platforms.svg').default,
    description: (
      <>
        Learn about the latest in humanoid robotics including reinforcement learning, sim-to-real transfer,
        and major platforms from Boston Dynamics, Honda, and Tesla.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
