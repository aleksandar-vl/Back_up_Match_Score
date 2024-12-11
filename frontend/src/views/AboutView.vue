<template>
    <HeaderSection />

  <div class="content-wrapper">
    <div class="all-cards">
      <!-- Welcome Card -->
      <div class="welcome-card">
        <div class="welcome-content">
          <h1 class="title">
            <i class="mdi mdi-cat" style="margin-right: 8px;"></i>
            Welcome to Kitten Strike!
          </h1>
          <p class="subtitle">Where feline reflexes meet esports!</p>
        </div>
      </div>

      <div class="main-content">
        <!-- What is Kitten Strike -->
        <div class="info-card full-width">
          <h2 class="section-title">
            <i class="mdi mdi-gamepad-variant" style="margin-right: 8px;"></i>
            What is Kitten Strike?
          </h2>
          <p class="description">
            Imagine Counter-Strike, but instead of regular characters, you have kittens with tactical vests and laser pointers!
            This is a game where precision is as important as the afternoon nap, and strategy is more delicious than a bowl of tuna.
          </p>
          <div class="features" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
            <div class="feature-item">
              <i class="mdi mdi-target" style="color: #42DDF2FF;"></i>
              <span>Precise aiming with laser pointers</span>
            </div>
            <div class="feature-item">
              <i class="mdi mdi-run-fast" style="color: #42DDF2FF;"></i>
              <span>Feline reflexes and acrobatic skills</span>
            </div>
            <div class="feature-item">
              <i class="mdi mdi-account-group" style="color: #42DDF2FF;"></i>
              <span>Team play and tactical purring</span>
            </div>
            <div class="feature-item">
              <i class="mdi mdi-medal" style="color: #FED854FF;"></i>
              <span>Compete for prestigious prizes</span>
            </div>
            <div class="feature-item">
              <i class="mdi mdi-trophy" style="color: #FED854FF;"></i>
              <span>Participate in various tournament formats</span>
            </div>
            <div class="feature-item">
              <i class="mdi mdi-lightning-bolt" style="color: #FED854FF;"></i>
              <span>Intense head-to-head matchups</span>
            </div>
          </div>
        </div>

        <div class="second-row" style="display: flex; gap: 24px;">
          <!-- Tournament Formats -->
          <div class="tournament-card" style="flex: 1;">
            <h2 class="section-title">
              <i class="mdi mdi-trophy" style="margin-right: 8px;"></i>
              Tournament Formats
            </h2>
            <div class="tournament-types">
              <div class="tournament-type">
                <div class="tournament-info">
                  <h3>Single Elimination</h3>
                  <p>Supports 4 or 8 teams battling their way through Quarter Finals, Semi Finals and the ultimate Grand Final. All matches are MR15 format - first team to 16 rounds wins!</p>
                </div>
              </div>
              <div class="tournament-type">
                <div class="tournament-info">
                  <h3>Round Robin</h3>
                  <p>Perfect for 4 or 5 teams where everyone faces off against each other in action-packed MR12 format matches during the intense Group Stage, followed by an epic Grand Finals clash in MR15!</p>
                </div>
              </div>
              <div class="tournament-type">
                <div class="tournament-info">
                  <h3>One Off Match</h3>
                  <p>The perfect high-stakes format for an intense head-to-head battle where legends are born and only one team emerges victorious! Every round counts!</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Tournament Stages -->
          <div class="stages-info" style="flex: 1;">
            <h2 class="section-title">
              <i class="mdi mdi-flag-checkered" style="margin-right: 8px;"></i>
              Tournament Stages
            </h2>
            <div class="stages-grid">
              <div class="stage-item">
                <h4>Group Stage <span class="stage-duration">(2 days)</span></h4>
                <p>A chaotic whisker-to-whisker battle where every kitten faces off against each other!</p>
              </div>
              <div class="stage-item">
                <h4>Quarter Finals <span class="stage-duration">(2 days)</span></h4>
                <p>First major challenge in Single Elimination format!</p>
              </div>
              <div class="stage-item">
                <h4>Semi Finals <span class="stage-duration">(1 day)</span></h4>
                <p>The penultimate battle before glory!</p>
              </div>
              <div class="stage-item">
                <h4>Finals <span class="stage-duration">(Same day)</span></h4>
                <p>The ultimate showdown for the championship!</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Prizes -->
        <div class="prizes-card">
          <h2 class="section-title">
            <i class="mdi mdi-gift" style="margin-right: 8px;"></i>
            Prizes
          </h2>
          <p class="description">
            In Kitten Strike, prizes aren't just trophies - they're real treasures! Winners receive prestigious "Kitty Kibbles" - special currency that can be used to purchase equipment, cosmetic items, and many other feline goodies!
          </p>
          <div class="prizes-list">
            <div class="prize-item">
              <i class="mdi mdi-trophy" color="#FED854FF"></i>
              <span>1st Place: Golden Fish Bowl Trophy</span>
            </div>
            <div class="prize-item">
              <i class="mdi mdi-trophy" color="#C0C0C0"></i>
              <span>2nd Place: Silver Milk Saucer</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import HeaderSection from "@/components/HeaderSection.vue";
</script>

<style scoped>

.content-wrapper {
  position: relative;
  z-index: 3;
  padding-top: 100px;
  flex-direction: column;
  gap: 20px;
  width: 100vw;
  justify-items: center;
}

.all-cards {
  display: flex;
  flex-direction: column;
  max-width: 1000px;
}

.welcome-card,
.info-card,
.tournament-card,
.prizes-card,
.stages-info {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
  margin-bottom: 24px;
  width: 100%;
  text-align: center;
}

.welcome-content {
  text-align: center;
}

.title {
  color: #42DDF2FF;
  font-size: 2rem;
  margin: 0;
}

.subtitle {
  color: #FED854FF;
  font-size: 1.2rem;
  margin-top: 8px;
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.second-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  align-items: stretch;
}

.section-title {
  color: #42DDF2FF;
  font-size: 1.5rem;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.description {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 20px;
  line-height: 1.6;
}

.features,
.tournament-types,
.prizes-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  background: rgba(66, 221, 242, 0.1);
  transition: all 0.2s;
  color: white;
}

.tournament-type,
.prize-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  background: rgba(254, 216, 84, 0.1);
  transition: all 0.2s;
}

.tournament-info {
  flex: 1;
}

.tournament-info h3 {
  color: #FED854FF;
  margin: 0 0 4px 0;
  font-size: 1.2rem;
}

.tournament-info p {
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-size: 0.9rem;
}

.prize-item {
  color: #FED854FF;
}

.prize-item:last-child {
  background: rgba(192, 192, 192, 0.1);
  color: #C0C0C0;
}

.stages-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 16px;
}

.stage-item {
  background: rgba(66, 221, 242, 0.1);
  padding: 16px;
  border-radius: 8px;
  text-align: center;
}

.stage-item h4 {
  color: #42DDF2FF;
  margin-bottom: 8px;
}

.stage-duration {
  font-size: 0.9em;
  color: #FED854FF;
}

.stage-item p {
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}
</style>
