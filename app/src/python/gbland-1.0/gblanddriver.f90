subroutine latlon2land(glat,glon,dtl)

      use dist2Coast

!f2py real intent(in) :: glon,glat
!f2py real intent(out) :: dtl

      call gbland(glon,glat,dtl)

end subroutine latlon2land


