# Mobile Breakpoint Testing Guidelines

When evaluating the UI for CapacitorJS mobile environments (iOS and Android), follow these recursive breakpoint testing strategies:

## 1. Native Viewport Assumptions
- Never assume `100vh` maps correctly to the visible screen area. Mobile browsers and native app wrappers (like iOS Safari and Capacitor) often have overlapping UI elements (address bars, bottom navigation).
- **Rule:** Always use dynamic viewport height `min-h-[100dvh]` or `h-[100dvh]` to account for dynamic toolbars.

## 2. Safe Areas
- Devices with notches or home indicators require safe area padding to prevent UI from being obscured.
- Ensure Tailwind's padding utilities (e.g., `pt-safe`, `pb-safe`) are configured or use standard CSS env variables:
  ```css
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  ```

## 3. Breakpoint Strategy
Test the UI actively across these key simulated breakpoints:
- **Small Mobile (sm):** 320px - 375px (iPhone SE, older Android devices)
  - Ensure touch targets are at least 44x44px.
  - Text remains readable without horizontal scrolling.
- **Large Mobile (md):** 390px - 430px (iPhone 14/15 Pro Max, large Androids)
  - Layout doesn't stretch awkwardly.
  - Modals and popovers fit within the screen boundaries.
- **Tablet (lg):** 768px - 1024px (iPads, large tablets)
  - Multi-column layouts behave properly.

## 4. Touch Interactions
- Verify hover states are replaced by or accompanied by active/focus states on mobile devices since hover is not native to touch.
- Prevent double-tap zooming by ensuring `user-scalable=no` is in the viewport meta tag.
- Test scrollable areas to ensure momentum scrolling works (`-webkit-overflow-scrolling: touch`).

## 5. Testing Tools
- Use Chrome DevTools Device Toolbar.
- Test directly via XCode Simulator (iOS) and Android Studio Emulator.
- Use `npm run dev -- --host` to test on a physical device on the same local network.
