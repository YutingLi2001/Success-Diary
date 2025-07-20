# ADR-0007: Analytics Architecture with Chart.js Integration

## Status

Accepted

## Context

The Success-Diary application requires a data visualization system for user analytics and mood tracking. Key considerations include:

- **Framework Choice**: Chart.js already selected for frontend visualization
- **Data Volume**: Personal journaling data with moderate volume per user
- **Performance**: Smooth chart rendering without backend bottlenecks
- **Real-time Updates**: Charts should reflect new entries immediately
- **Scalability**: Architecture should support growing user base

## Decision

Implement hybrid aggregated API with client-side rendering:

- **Backend Strategy**: FastAPI endpoints return pre-aggregated analytics data
- **Frontend Rendering**: Chart.js handles visualization with smooth animations
- **Caching Layer**: Redis/memory cache for aggregated data (5-minute TTL)
- **Real-time Updates**: WebSocket notifications for live data when user creates entries

## Considered Options

1. **Server-side chart generation**: Backend generates image charts, simple but inflexible
2. **Client-side raw data**: Send raw entries to frontend, flexible but performance issues
3. **Hybrid aggregated API (Selected)**: Pre-aggregated data with client rendering
4. **Third-party analytics**: External service integration, but data privacy concerns
5. **Real-time streaming**: WebSocket data streaming, complex but unnecessary for journaling

## Consequences

**Positive:**
- Optimized data transfer reduces bandwidth usage
- Interactive charts with smooth animations and transitions
- Efficient server processing with intelligent caching
- Real-time feel without constant API polling
- Scalable architecture supports user growth

**Negative:**
- Additional caching infrastructure complexity
- WebSocket implementation adds technical overhead
- Cache invalidation logic required for data consistency

**Neutral:**
- Standard pattern for modern web applications
- Well-supported by Chart.js and FastAPI

## Implementation Notes

**Backend API Design:**
```python
# FastAPI analytics endpoints
@app.get("/analytics/mood-trends")
async def get_mood_trends(
    days: int = 30, 
    user: User = Depends(current_user)
):
    # Check cache first
    cache_key = f"mood_trends:{user.id}:{days}"
    cached_data = await redis.get(cache_key)
    
    if cached_data:
        return json.loads(cached_data)
    
    # Generate aggregated data
    entries = await get_user_entries_for_period(user.id, days)
    trend_data = {
        "labels": [entry.created_at.strftime("%Y-%m-%d") for entry in entries],
        "datasets": [{
            "label": "Overall Rating",
            "data": [entry.overall_rating for entry in entries],
            "borderColor": "rgb(59, 130, 246)",
            "backgroundColor": "rgba(59, 130, 246, 0.1)"
        }]
    }
    
    # Cache for 5 minutes
    await redis.setex(cache_key, 300, json.dumps(trend_data))
    return trend_data
```

**Frontend Chart Configuration:**
```javascript
// Chart.js configuration
const chartConfig = {
  type: 'line',
  data: await fetchAnalyticsData('/analytics/mood-trends'),
  options: {
    responsive: true,
    maintainAspectRatio: false,
    animation: { 
      duration: 800,
      easing: 'easeInOutQuart'
    },
    interaction: { 
      intersect: false,
      mode: 'index'
    },
    plugins: {
      tooltip: {
        enabled: true,
        mode: 'nearest'
      }
    }
  }
};

// Real-time updates via WebSocket
websocket.addEventListener('message', (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'entry_created') {
    refreshChartData();
  }
});
```

**Caching Strategy:**
- **Cache Duration**: 5-minute TTL for balance between freshness and performance
- **Cache Keys**: User-specific with parameter variations
- **Invalidation**: Clear cache on entry creation/modification
- **Memory Management**: Redis with appropriate memory limits

**Analytics Endpoints:**
- `/analytics/mood-trends` - Daily mood progression
- `/analytics/gratitude-frequency` - Gratitude entry patterns
- `/analytics/anxiety-patterns` - Anxiety level tracking
- `/analytics/journal-activity` - Writing frequency and volume

## References

- Chart.js documentation and performance best practices
- FastAPI caching patterns with Redis
- WebSocket real-time update implementations
- Original analysis: `docs/requirements/remaining_requirements_analysis.md` (Section 5)