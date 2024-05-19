
#include <deque>

class CurrentPerformanceChecker {
private:
  std::deque<bool> within_threshold;
  size_t capacity;

public:
  CurrentPerformanceChecker(size_t capacity) : capacity(capacity) {}
  void add(bool value) {
    within_threshold.push_back(value);
    if (within_threshold.size() > capacity) {
      within_threshold.pop_front();
    }
  }

  size_t getSize() { return capacity; }

  float getPercentage() const {
    size_t trueCount = 0;
    for (bool val : within_threshold) {
      if (val) {
        trueCount++;
      }
    }
    return static_cast<float>(trueCount) / within_threshold.size();
  }
};