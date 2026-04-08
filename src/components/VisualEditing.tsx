import { useEffect } from 'react'
import { enableVisualEditing } from '@sanity/visual-editing'

// Componente React island que activa los overlays de edición.
// Solo hace algo cuando la página se abre desde el Presentation Tool del Studio.
export default function VisualEditing() {
  useEffect(() => {
    const cleanup = enableVisualEditing()
    return cleanup
  }, [])
  return null
}
