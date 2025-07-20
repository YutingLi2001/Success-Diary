# ADR-0008: Data Export Strategy - CSV First Approach

## Status

Accepted

## Context

The Success-Diary application needs data export functionality for V3.0+ to allow users to backup and analyze their journaling data. Key considerations include:

- **User Demographics**: Target users (personal growth enthusiasts) prefer spreadsheet-compatible formats
- **Use Cases**: Data analysis, backup, migration, sharing with therapists/coaches
- **Technical Complexity**: Balance between comprehensive exports and implementation simplicity
- **Format Compatibility**: Universal accessibility across different platforms and tools
- **Future Extensibility**: Foundation for additional export formats

## Decision

Implement CSV export as primary format with JSON planned for future releases:

- **Primary Format**: CSV for V3.0 initial data export release
- **Structure**: Flattened data optimized for spreadsheet analysis
- **Future Enhancement**: JSON format in V3.1 for power users and API integration
- **Export Scope**: Complete user data with optional date range filtering

## Considered Options

1. **JSON only**: Developer-friendly but limited accessibility for target users
2. **CSV only**: Universal compatibility but limited for complex data structures
3. **CSV first, JSON later (Selected)**: Broad appeal with clear upgrade path
4. **Multiple formats immediately**: Comprehensive but complex initial implementation
5. **PDF export**: Human-readable but not suitable for data analysis

## Consequences

**Positive:**
- Universal compatibility with Excel, Google Sheets, and other spreadsheet tools
- Immediate data analysis capability for casual users
- Broader user appeal within journaling demographic
- Simple implementation with clear upgrade path to additional formats
- Familiar format for users sharing data with professionals

**Negative:**
- CSV format limitations for complex nested data structures
- Loss of some metadata and relationships in flattened format
- Additional implementation needed for comprehensive data export

**Neutral:**
- Standard approach for user-facing data exports
- Well-supported by FastAPI and Python ecosystem

## Implementation Notes

**CSV Export Format:**
```csv
Date,Victory,Gratitude,Anxiety,Overall_Rating,Journal_Text,Created_At,Modified_At
2025-01-15,"Completed project presentation","Supportive team feedback","Tight deadline stress",4,"Today felt productive despite the challenges...",2025-01-15T14:30:00Z,2025-01-15T14:30:00Z
2025-01-16,"Finished morning workout","Beautiful sunrise","None today",5,"Great start to the day with exercise...",2025-01-16T08:15:00Z,2025-01-16T08:15:00Z
```

**Backend Implementation:**
```python
import csv
from io import StringIO
from fastapi import Response

@app.get("/export/csv")
async def export_entries_csv(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    user: User = Depends(current_user)
):
    # Get user entries with optional date filtering
    entries = await get_user_entries_for_export(user.id, start_date, end_date)
    
    # Generate CSV content
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    
    # Header row
    writer.writerow([
        'Date', 'Victory', 'Gratitude', 'Anxiety', 'Overall_Rating', 
        'Journal_Text', 'Created_At', 'Modified_At'
    ])
    
    # Data rows
    for entry in entries:
        writer.writerow([
            entry.created_at.strftime('%Y-%m-%d'),
            entry.victory or '',
            entry.gratitude or '',
            entry.anxiety or '',
            entry.overall_rating or '',
            entry.journal_text or '',
            entry.created_at.isoformat(),
            entry.modified_at.isoformat() if entry.modified_at else ''
        ])
    
    csv_content = csv_buffer.getvalue()
    csv_buffer.close()
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=success_diary_export_{datetime.now().strftime('%Y%m%d')}.csv"
        }
    )
```

**Frontend Export Interface:**
```javascript
// Export functionality
const exportData = async (format = 'csv', dateRange = null) => {
  const params = new URLSearchParams();
  if (dateRange?.start) params.append('start_date', dateRange.start);
  if (dateRange?.end) params.append('end_date', dateRange.end);
  
  const response = await fetch(`/export/${format}?${params}`);
  const blob = await response.blob();
  
  // Trigger download
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `success_diary_export_${new Date().toISOString().split('T')[0]}.${format}`;
  a.click();
  window.URL.revokeObjectURL(url);
};
```

**Future JSON Format (V3.1):**
```json
{
  "export_metadata": {
    "generated_at": "2025-01-15T14:30:00Z",
    "user_id": "user123",
    "total_entries": 150,
    "date_range": {
      "start": "2024-01-01",
      "end": "2025-01-15"
    }
  },
  "entries": [
    {
      "id": "entry123",
      "date": "2025-01-15",
      "victory": "Completed project presentation",
      "gratitude": "Supportive team feedback",
      "anxiety": "Tight deadline stress",
      "overall_rating": 4,
      "journal_text": "Today felt productive despite...",
      "created_at": "2025-01-15T14:30:00Z",
      "modified_at": "2025-01-15T14:30:00Z"
    }
  ]
}
```

## References

- CSV format specifications (RFC 4180)
- FastAPI file response patterns
- Data export best practices for user-facing applications
- Original analysis: `docs/requirements/remaining_requirements_analysis.md` (Section 9)