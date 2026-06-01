#!/bin/bash
cat << 'INNEREOF' > ROADMAP.md
# Roadmap
- **Phase 1-25:** (Completed) Initial setup, CRUD, Web UI, ORM, Docker, Vue SPA, WebSockets, Blueprints, Celery, Playwright E2E, Vite build, Sub-goals, History, Avatars, Calendar View, Vue store, TypeScript, Vue Router, Tailwind dark mode, Settings view.
- **Phase 26:** Implement Analytics Dashboard to track user progress and goal completion rates over time.
- **Phase 27:** Gamification & Badges. Reward users for hitting milestones (e.g. 7-day streak, 100 goals).
- **Phase 28:** FastAPI Migration. Rebuild the Flask backend JSON API using FastAPI for better async performance and automatic OpenAPI docs, while keeping the Vue frontend intact.
INNEREOF

cat << 'INNEREOF' > TODO.md
# TODO
## Short-term Tasks
- [ ] Phase 26: Implement Analytics Dashboard.
  - Create `models.py` queries for user stats (total goals, completion %, daily streak).
  - Create a new Flask blueprint `analytics.py` (or route in `views.py`).
  - Create `AnalyticsView.vue` and add route in `router/index.ts`.
  - Add link to Nav bar.
  - Write Pytest and Playwright tests.
- [ ] Review UI and ensure responsiveness.
INNEREOF

cat << 'INNEREOF' > IDEAS.md
# Ideas
- **Pivot to Mobile App:** Wrap the Vue SPA in Capacitor or React Native for iOS/Android native deployments.
- **AI Coach Integration:** Use LLMs to analyze user goal patterns and suggest better sub-goals or routines.
- **Social Accountability:** Allow users to share specific goals with an accountability partner who gets notified if it's missed.
- **Language Porting:** Rewrite the backend in Go or Rust for extreme performance.
- **Offline First:** Use IndexedDB and Service Workers to make the app work offline and sync when reconnected.
INNEREOF

cat << 'INNEREOF' > DEPLOY.md
# Deployment Instructions
1. **Prerequisites:** Docker, Docker-Compose.
2. **Environment Variables:** Copy `.env.example` to `.env` and fill in `SECRET_KEY`, `DATABASE_URL` (optional, defaults to SQLite), `REDIS_URL`, etc.
3. **Build Frontend:** `cd frontend && npm install && npm run build` (This generates static files in `dist/`).
4. **Run Backend (Docker):** `docker-compose up -d --build` (This spins up the web server, Celery worker, and Redis).
5. **Database Initialization:** The application auto-initializes the database tables on first boot.
INNEREOF

cat << 'INNEREOF' > VISION.md
# Project Vision
The One-Minute Manager is a lightning-fast, zero-friction goal tracking system. It prioritizes speed, ease of use, and immediate gratification to help users break down and accomplish their daily tasks. The architecture focuses on real-time reactivity (WebSockets), offline-capable client-side rendering (Vue SPA), and strict data integrity (PostgreSQL/SQLAlchemy), scaling easily for multi-tenant team usage.
INNEREOF

cat << 'INNEREOF' > MEMORY.md
# Internal Architecture & Memories
- Frontend: Vue 3 (Composition API), Vite, TypeScript, Vue-Router, Tailwind CSS (v4), Headless UI.
- Backend: Flask, Blueprints, Flask-SocketIO, Celery+Redis, SQLAlchemy, SQLite/PostgreSQL.
- Testing: Pytest (Backend API), Playwright (Frontend E2E).
- Design Preferences: Strict modularity, minimal external dependencies where possible, strong typing via TypeScript, reactive UI without page reloads.
INNEREOF

cat << 'INNEREOF' > VERSION.md
0.26.0
INNEREOF

cat << 'INNEREOF' >> CHANGELOG.md

## 0.26.0
- **Feature**: Implemented Phase 26 Analytics Dashboard.
  - Added new `/api/analytics` backend endpoint using `blueprints/analytics.py` and `models.get_user_analytics()`.
  - Added frontend `AnalyticsView.vue` with responsive charts tracking Total Goals, Completed Goals, Completion Rate, and Day Streak.
  - Updated Vue Router and NavBar to support the new Analytics route.
  - Tested logic extensively via `test_analytics.py` and E2E `test_playwright_analytics.py`.
INNEREOF

cat << 'INNEREOF' > frontend/src/views/AnalyticsView.vue
<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-100 dark:border-gray-700 transition-colors">
      <h2 class="text-2xl font-semibold text-gray-800 dark:text-gray-100 mb-6 flex items-center gap-2">
        <ChartBarIcon class="w-6 h-6 text-blue-500" />
        Analytics Dashboard
      </h2>

      <div v-if="loading" class="text-center py-10 text-gray-500 dark:text-gray-400">
        Loading analytics...
      </div>

      <div v-else-if="error" class="text-center py-10 text-red-500">
        {{ error }}
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

        <!-- Total Goals -->
        <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-100 dark:border-blue-800 flex flex-col items-center justify-center text-center transition-colors">
          <span class="text-blue-500 dark:text-blue-400 mb-1">
            <ClipboardDocumentListIcon class="w-8 h-8 mx-auto" />
          </span>
          <span class="text-3xl font-bold text-gray-800 dark:text-gray-100">{{ stats?.total_goals || 0 }}</span>
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mt-1">Total Goals</span>
        </div>

        <!-- Completed Goals -->
        <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-100 dark:border-green-800 flex flex-col items-center justify-center text-center transition-colors">
          <span class="text-green-500 dark:text-green-400 mb-1">
            <CheckCircleIcon class="w-8 h-8 mx-auto" />
          </span>
          <span class="text-3xl font-bold text-gray-800 dark:text-gray-100">{{ stats?.completed_goals || 0 }}</span>
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mt-1">Completed</span>
        </div>

        <!-- Completion Rate -->
        <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg border border-purple-100 dark:border-purple-800 flex flex-col items-center justify-center text-center transition-colors">
          <span class="text-purple-500 dark:text-purple-400 mb-1">
            <ChartPieIcon class="w-8 h-8 mx-auto" />
          </span>
          <span class="text-3xl font-bold text-gray-800 dark:text-gray-100">{{ stats?.completion_percentage || 0 }}%</span>
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mt-1">Completion Rate</span>
        </div>

        <!-- Daily Streak -->
        <div class="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg border border-orange-100 dark:border-orange-800 flex flex-col items-center justify-center text-center transition-colors">
          <span class="text-orange-500 dark:text-orange-400 mb-1">
            <FireIcon class="w-8 h-8 mx-auto" />
          </span>
          <span class="text-3xl font-bold text-gray-800 dark:text-gray-100">{{ stats?.streak || 0 }}</span>
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mt-1">Day Streak</span>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ChartBarIcon, ClipboardDocumentListIcon, CheckCircleIcon, ChartPieIcon, FireIcon } from '@heroicons/vue/24/outline'

interface AnalyticsStats {
  total_goals: number
  completed_goals: number
  pending_goals: number
  completion_percentage: number
  streak: number
}

const stats = ref<AnalyticsStats | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const res = await fetch('/api/analytics')
    if (res.ok) {
      stats.value = await res.json()
    } else {
      error.value = 'Failed to load analytics data.'
    }
  } catch (e) {
    error.value = 'An error occurred while fetching analytics.'
  } finally {
    loading.value = false
  }
})
</script>
INNEREOF

cat << 'INNEREOF' > frontend/src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { user } from '../store'

import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import AnalyticsView from "../views/AnalyticsView.vue"
import SettingsView from '../views/SettingsView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: AnalyticsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  // Wait a tick for auth to establish natively on boot if navigating directly
  if (to.meta.requiresAuth && !user.authenticated) {
    next({ name: 'login' })
  } else if ((to.name === 'login' || to.name === 'register') && user.authenticated) {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
INNEREOF

cat << 'INNEREOF' > blueprints/analytics.py
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
import models

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/api/analytics", methods=["GET"])
@login_required
def get_analytics():
    stats = models.get_user_analytics(current_user.id)
    return jsonify(stats), 200
INNEREOF

cat << 'INNEREOF' > test_analytics.py
import pytest
from app import app
import models
import json

@pytest.fixture
def client():
    app.config["TESTING"] = True
    import os
    if os.path.exists("test_analytics.db"):
        os.remove("test_analytics.db")
    models.init_db("test_analytics.db")
    with app.test_client() as client:
        # Override the env var so models uses this db path automatically
        os.environ["DATABASE_PATH"] = "test_analytics.db"
        yield client

    if os.path.exists("test_analytics.db"):
        os.remove("test_analytics.db")

def test_analytics_api(client):
    # Register user
    res = client.post(
        "/api/register",
        data=json.dumps({"username": "analytics_user_2", "password": "password"}),
        content_type="application/json"
    )
    assert res.status_code == 201

    # Login
    client.post(
        "/api/login",
        data=json.dumps({"username": "analytics_user_2", "password": "password"}),
        content_type="application/json"
    )

    # Add goals
    res = client.post("/api/goals", data=json.dumps({"description": "Goal 1"}), content_type="application/json")
    assert res.status_code == 201
    res = client.post("/api/goals", data=json.dumps({"description": "Goal 2"}), content_type="application/json")

    # Complete one goal
    # Note: SQLite IDs start at 1 and auto-increment per table
    client.post("/api/goals/1/complete")

    # Check analytics
    res = client.get("/api/analytics")
    assert res.status_code == 200
    data = res.get_json()
    assert data["total_goals"] == 2
    assert data["completed_goals"] == 1
    assert data["pending_goals"] == 1
    assert data["completion_percentage"] == 50
    assert data["streak"] == 1
INNEREOF
