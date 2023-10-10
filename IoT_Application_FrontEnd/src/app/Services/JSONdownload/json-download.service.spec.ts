import { TestBed } from '@angular/core/testing';

import { JsonDownloadService } from './json-download.service';

describe('JsonDownloadService', () => {
  let service: JsonDownloadService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(JsonDownloadService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
