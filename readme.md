<h1> Reinforcement learning </h1>

<h2> example </h2>
<p> 책에서 제공하는 DeepSarsa 알고리즘 기본 파일</p>

<h2> pure python </h2>
<p> pygame_1에서 pygame으로 이루어진 environment를 순수 파이썬 코드로 대체해 만든 파일</p>

<h2> pygame_1 </h2>
<p> 기존에 제작하던 프로젝트 </p>

<h2> pygame_2 </h2>
<p> examplr 파일의 DeepSarsaAgent 클래스를 그래도 사용해 학습할 수 있도록 만든 게임 </p>
<p>1. environment_1: 움직이는 초록 물체를 피해 파랑색에 도착하는 방식</p>
<p>2. environment_2: 그냥 파란색에 도착하는 방식  </p>
<p>main.py에 둘 중 하나를 import 하면 된다.</p>
<p>record는 environment_2의 학습 횟수에 따른 플레이 시간 그래프. Y값이 적을 수록 좋은 AI이다.
environment_2 수준의 게임은 학습이 가능한 것으로 보인다.
</p>
<hr>
<h1> 문제점 </h1>
<p>
example 파일의 DeepSarsaAgent를 적용해보아도 학습이 잘 되지 않는다.
학습 agent만 문제인 것은 아닌거 같고 학습 환경 코드에도 문제가 있는 것 같다.
</p>

<p>
알고리즘인 DeepSarsa의 문제일 수도 있다. DQN이나 Reinforcement 등, 다른 알고리즘을 시도해볼 수도 있을 듯
</p>